"""Event bus implementation for domain events."""
from typing import Callable, Dict, List, Optional
from src.domain.events.events import DomainEvent, EventType
import asyncio
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """
    In-memory event bus for publishing and subscribing to domain events.
    
    Supports both synchronous and asynchronous handlers.
    Follows the mediator pattern for decoupled event handling.
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._async_subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[DomainEvent] = []
        self._max_history_size: int = 1000
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable[[DomainEvent], None],
    ) -> None:
        """
        Subscribe a synchronous handler to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Synchronous handler function
        """
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed handler to event type: {event_type}")
    
    def subscribe_async(
        self,
        event_type: str,
        handler: Callable[[DomainEvent], asyncio.Task],
    ) -> None:
        """
        Subscribe an asynchronous handler to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Asynchronous handler function
        """
        self._async_subscribers[event_type].append(handler)
        logger.debug(f"Subscribed async handler to event type: {event_type}")
    
    def unsubscribe(
        self,
        event_type: str,
        handler: Callable,
    ) -> None:
        """
        Unsubscribe a handler from an event type.
        
        Args:
            event_type: Type of event
            handler: Handler function to remove
        """
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            logger.debug(f"Unsubscribed handler from event type: {event_type}")
    
    def publish(self, event: DomainEvent) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        # Store in history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history_size:
            self._event_history.pop(0)
        
        # Get all handlers for this event type
        event_type = event.event_type.value
        handlers = self._subscribers.get(event_type, [])
        
        # Also check for wildcard subscribers
        handlers.extend(self._subscribers.get("*", []))
        
        # Call synchronous handlers
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")
        
        # Schedule asynchronous handlers
        async_handlers = self._async_subscribers.get(event_type, [])
        async_handlers.extend(self._async_subscribers.get("*", []))
        
        if async_handlers:
            asyncio.create_task(self._dispatch_async(async_handlers, event))
        
        logger.debug(f"Published event: {event.event_type.value}")
    
    async def publish_async(self, event: DomainEvent) -> None:
        """
        Publish an event asynchronously.
        
        Args:
            event: Event to publish
        """
        self.publish(event)
    
    async def _dispatch_async(
        self,
        handlers: List[Callable],
        event: DomainEvent,
    ) -> None:
        """
        Dispatch event to asynchronous handlers.
        
        Args:
            handlers: List of async handlers
            event: Event to dispatch
        """
        tasks = []
        for handler in handlers:
            try:
                tasks.append(handler(event))
            except Exception as e:
                logger.error(f"Error scheduling async handler: {e}")
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Async handler error: {result}")
    
    def get_history(
        self,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[DomainEvent]:
        """
        Get event history.
        
        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        if event_type:
            filtered = [
                e for e in self._event_history
                if e.event_type.value == event_type
            ]
            return filtered[-limit:]
        return self._event_history[-limit:]
    
    def clear_history(self) -> None:
        """Clear event history."""
        self._event_history.clear()
    
    def get_subscriber_count(self, event_type: str) -> int:
        """
        Get number of subscribers for an event type.
        
        Args:
            event_type: Type of event
            
        Returns:
            Number of subscribers
        """
        return len(self._subscribers.get(event_type, []))


__all__ = ["EventBus"]