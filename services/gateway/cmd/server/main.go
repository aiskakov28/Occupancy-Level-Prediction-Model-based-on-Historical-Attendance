package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
)

var forecastURL = env("FORECAST_URL", "http://localhost:8000")

func env(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}

func cors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Access-Control-Allow-Methods", "GET,OPTIONS")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func proxyForecast(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("hours")
	if q == "" {
		q = "24"
	}
	resp, err := http.Get(forecastURL + "/forecast/hourly?hours=" + q)
	if err != nil {
		http.Error(w, "upstream error", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	_, _ = io.Copy(w, resp.Body)
}

func current(w http.ResponseWriter, r *http.Request) {
	resp, err := http.Get(forecastURL + "/forecast/hourly?hours=1")
	if err != nil {
		http.Error(w, "upstream error", http.StatusBadGateway)
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

func health(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write([]byte(`{"ok":true}`))
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", health)
	mux.HandleFunc("/api/forecast/hourly", proxyForecast)
	mux.HandleFunc("/api/occupancy/current", current)

	addr := ":" + env("PORT", "8080")
	log.Println("gateway listening on", addr, "->", forecastURL)
	log.Fatal(http.ListenAndServe(addr, cors(mux)))
}
