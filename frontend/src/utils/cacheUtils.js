// Utility functions for cache management
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes for weather data
const NEWS_CACHE_DURATION = 2 * 60 * 60 * 1000; // 2 hours for news

// Clean up expired cache entries
export const cleanExpiredCache = () => {
  const keys = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && (key.includes('weatherCache_') || key.includes('weatherWave_'))) {
      keys.push(key);
    }
  }

  let cleanedCount = 0;
  keys.forEach(key => {
    try {
      const value = localStorage.getItem(key);
      const data = JSON.parse(value);
      if (data.timestamp) {
        const duration = key.includes('news') ? NEWS_CACHE_DURATION : CACHE_DURATION;
        if (Date.now() - data.timestamp > duration) {
          localStorage.removeItem(key);
          cleanedCount++;
        }
      }
    } catch (e) {
      // Remove invalid cache entries
      localStorage.removeItem(key);
      cleanedCount++;
    }
  });

  if (cleanedCount > 0) {
    console.log(`🧹 Cleaned ${cleanedCount} expired cache entries`);
  }
};

// Get cache size info
export const getCacheInfo = () => {
  let totalSize = 0;
  let itemCount = 0;
  
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && (key.includes('weatherCache_') || key.includes('weatherWave_'))) {
      const value = localStorage.getItem(key);
      totalSize += new Blob([value]).size;
      itemCount++;
    }
  }
  
  return {
    itemCount,
    totalSize: (totalSize / 1024).toFixed(1) + ' KB'
  };
};

// Clean all cache
export const clearAllCache = () => {
  const keys = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && (key.includes('weatherCache_') || key.includes('weatherWave_'))) {
      keys.push(key);
    }
  }
  keys.forEach(key => localStorage.removeItem(key));
  console.log(`🗑️ Cleared ${keys.length} cache entries`);
};
