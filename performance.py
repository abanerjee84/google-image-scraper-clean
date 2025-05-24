"""
Performance monitoring utilities for Google Image Scraper
"""
import time
import psutil
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    memory_usage_mb: float = 0.0
    cpu_percent: float = 0.0
    urls_found: int = 0
    images_downloaded: int = 0
    download_failures: int = 0
    search_term: str = ""
    
    def calculate_duration(self):
        """Calculate duration if end_time is set"""
        if self.end_time:
            self.duration = self.end_time - self.start_time
    
    def get_download_rate(self) -> float:
        """Calculate images downloaded per second"""
        if self.duration and self.duration.total_seconds() > 0:
            return self.images_downloaded / self.duration.total_seconds()
        return 0.0
    
    def get_success_rate(self) -> float:
        """Calculate download success rate as percentage"""
        total_attempts = self.images_downloaded + self.download_failures
        if total_attempts > 0:
            return (self.images_downloaded / total_attempts) * 100
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        self.calculate_duration()
        return {
            'search_term': self.search_term,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration.total_seconds() if self.duration else None,
            'memory_usage_mb': self.memory_usage_mb,
            'cpu_percent': self.cpu_percent,
            'urls_found': self.urls_found,
            'images_downloaded': self.images_downloaded,
            'download_failures': self.download_failures,
            'download_rate_per_second': self.get_download_rate(),
            'success_rate_percent': self.get_success_rate()
        }


class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.process = psutil.Process()
    
    def start_monitoring(self, task_id: str, search_term: str = "") -> PerformanceMetrics:
        """Start monitoring a task"""
        metrics = PerformanceMetrics(search_term=search_term)
        self.metrics[task_id] = metrics
        return metrics
    
    def update_system_metrics(self, task_id: str):
        """Update system resource usage metrics"""
        if task_id in self.metrics:
            try:
                # Get current memory usage
                memory_info = self.process.memory_info()
                self.metrics[task_id].memory_usage_mb = memory_info.rss / 1024 / 1024
                
                # Get CPU usage (this call may take up to 1 second)
                self.metrics[task_id].cpu_percent = self.process.cpu_percent()
            except psutil.Error:
                # Handle cases where process info is not available
                pass
    
    def finish_monitoring(self, task_id: str):
        """Finish monitoring a task"""
        if task_id in self.metrics:
            self.metrics[task_id].end_time = datetime.now()
            self.metrics[task_id].calculate_duration()
            self.update_system_metrics(task_id)
    
    def get_metrics(self, task_id: str) -> Optional[PerformanceMetrics]:
        """Get metrics for a specific task"""
        return self.metrics.get(task_id)
    
    def get_all_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Get all tracked metrics"""
        return self.metrics.copy()
    
    def print_summary(self, task_id: str):
        """Print a summary of performance metrics"""
        metrics = self.get_metrics(task_id)
        if not metrics:
            print(f"No metrics found for task: {task_id}")
            return
        
        metrics.calculate_duration()
        duration_str = str(metrics.duration).split('.')[0] if metrics.duration else "Unknown"
        
        print(f"\n📊 Performance Summary for '{metrics.search_term}':")
        print(f"   ⏱️  Duration: {duration_str}")
        print(f"   💾 Memory Usage: {metrics.memory_usage_mb:.1f} MB")
        print(f"   🖥️  CPU Usage: {metrics.cpu_percent:.1f}%")
        print(f"   🔗 URLs Found: {metrics.urls_found}")
        print(f"   📥 Images Downloaded: {metrics.images_downloaded}")
        print(f"   ❌ Download Failures: {metrics.download_failures}")
        print(f"   📈 Download Rate: {metrics.get_download_rate():.2f} images/second")
        print(f"   ✅ Success Rate: {metrics.get_success_rate():.1f}%")


@asynccontextmanager
async def monitor_performance(monitor: PerformanceMonitor, task_id: str, search_term: str = ""):
    """Async context manager for performance monitoring"""
    metrics = monitor.start_monitoring(task_id, search_term)
    try:
        yield metrics
    finally:
        monitor.finish_monitoring(task_id)


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


async def benchmark_scraping_task(search_term: str, count: int = 10):
    """
    Benchmark a scraping task and return performance metrics
    
    Args:
        search_term: The search term to scrape
        count: Number of images to download
        
    Returns:
        PerformanceMetrics object with results
    """
    from GoogleImageScraper import find_image_urls, save_images
    
    task_id = f"benchmark_{search_term}_{int(time.time())}"
    
    async with monitor_performance(performance_monitor, task_id, search_term) as metrics:
        try:
            # Find URLs
            image_urls = await find_image_urls(
                search_key=search_term,
                number_of_images=count,
                headless=True
            )
            metrics.urls_found = len(image_urls)
            
            if image_urls:
                # Download images
                downloaded, failed = await save_images(
                    image_urls=image_urls,
                    images_dir_path=f'benchmark_photos/{search_term}',
                    image_file_prefix=search_term
                )
                metrics.images_downloaded = downloaded
                metrics.download_failures = failed
                
        except Exception as e:
            print(f"Benchmark failed for {search_term}: {e}")
    
    performance_monitor.print_summary(task_id)
    return metrics
