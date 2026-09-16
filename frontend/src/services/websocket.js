export class MonitoringWebSocket {
  constructor(onMessage, onError, onStatusChange) {
    this.url = 'ws://127.0.0.1:8000/api/ws/monitoring';
    this.ws = null;
    this.onMessage = onMessage;
    this.onError = onError;
    this.onStatusChange = onStatusChange;
    this.isConnected = false;
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        if (this.onStatusChange) this.onStatusChange(true);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.onMessage) this.onMessage(data);
        } catch (err) {
          console.error('[WebSocket] Parsing error:', err);
        }
      };

      this.ws.onerror = (error) => {
        if (this.onError) this.onError(error);
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        if (this.onStatusChange) this.onStatusChange(false);
      };
    } catch (e) {
      console.error('[WebSocket] Connection failed:', e);
      if (this.onStatusChange) this.onStatusChange(false);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
    if (this.onStatusChange) this.onStatusChange(false);
  }
}
