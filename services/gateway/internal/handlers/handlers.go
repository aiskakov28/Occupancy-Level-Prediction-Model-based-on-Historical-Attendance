package handlers

import (
	"encoding/json"
	"io"
	"net/http"
)

type Gateway struct {
	ForecastURL string
}

func (g Gateway) Health(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write([]byte(`{"ok":true}`))
}

func (g Gateway) Forecast(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("hours")
	if q == "" {
		q = "24"
	}
	resp, err := http.Get(g.ForecastURL + "/forecast/hourly?hours=" + q)
	if err != nil {
		http.Error(w, "upstream", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	_, _ = io.Copy(w, resp.Body)
}

func (g Gateway) Current(w http.ResponseWriter, _ *http.Request) {
	resp, err := http.Get(g.ForecastURL + "/forecast/hourly?hours=1")
	if err != nil {
		http.Error(w, "upstream", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	var arr []map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&arr); err != nil || len(arr) == 0 {
		http.Error(w, "bad upstream", http.StatusBadGateway)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(arr[0])
}
