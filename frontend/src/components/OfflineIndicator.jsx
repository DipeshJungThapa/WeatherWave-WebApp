// Simple offline indicator
import React from 'react';
import { Badge } from './ui/badge';
import { WifiOff, Wifi, Database } from 'lucide-react';

export const OfflineIndicator = ({ isOffline, isFromCache, className = "" }) => {
  if (!isOffline && !isFromCache) return null;

  return (
    <Badge 
      variant={isOffline ? "destructive" : "secondary"} 
      className={`flex items-center gap-1 ${className}`}
    >
      {isOffline ? (
        <>
          <WifiOff className="h-3 w-3" />
          Offline
        </>
      ) : isFromCache ? (
        <>
          <Database className="h-3 w-3" />
          Cached
        </>
      ) : (
        <>
          <Wifi className="h-3 w-3" />
          Live
        </>
      )}
    </Badge>
  );
};
