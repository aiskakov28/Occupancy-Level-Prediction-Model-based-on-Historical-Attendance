package iothttp

import (
	"context"
	"encoding/json"
	"net/http"
	"time"
)

type Event struct {
	TS       time.Time `json:"ts"`
	Count    int       `json:"count"`
	DeviceID string    `json:"device_id"`
	Source   string    `json:"source"`
}

func Start(ctx context.Context, addr string) <-chan Event {
	out := make(chan Event, 256)

	mux := http.NewServeMux()
	mux.HandleFunc("/ingest", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}
		var e Event
		if err := json.NewDecoder(r.Body).Decode(&e); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		if e.TS.IsZero() {
			e.TS = time.Now().UTC()
		} else {
			e.TS = e.TS.UTC()
		}
		if e.Source == "" {
			e.Source = "iot_http"
		}
		select {
		case out <- e:
			w.WriteHeader(http.StatusAccepted)
		default:
			w.WriteHeader(http.StatusTooManyRequests)
		}
	})

	srv := &http.Server{Addr: addr, Handler: mux}

	go func() { _ = srv.ListenAndServe() }()
	go func() {
		<-ctx.Done()
		_ = srv.Shutdown(context.Background())
		close(out)
	}()

	return out
}
