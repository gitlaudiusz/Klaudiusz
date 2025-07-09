# Command A-03-2025: Troubleshooting Report

**Data**: 2025-07-03 18:30:00
**Model**: Command A-03-2025 (LibraxisAI)
**Status**: Server uruchomiony ale nie odpowiada na żadne endpointy

## Próby połączenia
- `/v1/chat/completions` - 404 Not Found
- `/chat/completions` - 404 Not Found  
- `/` - 404 Not Found
- `/generate` - 404 Not Found
- `/v1/completions` - 404 Not Found

## Działające endpointy
- `/health` - 200 OK {"status": "ok"}

## Proces serwera
Server działa na porcie 53173, proces ID: 68623
```
/Users/polyversai/Codebase/Klaudiusz/mlx_lm/.venv/bin/python /Users/polyversai/Codebase/Klaudiusz/mlx_lm/.venv/bin/mlx_lm.server --model /Users/polyversai/.lmstudio/models/LibraxisAI/c4ai-command-a-03-2025-q5-mlx --host 0.0.0.0 --port 53173 --trust-remote-code
```

## Możliwe przyczyny
1. Model może nie zostać poprawnie załadowany
2. Endpoint API może być inny niż standardowe OpenAI
3. Może potrzebować dłuższego czasu na inicjalizację
4. Może wystąpić problem z kompatybilnością MLX

## Następne kroki
- Sprawdzić logi serwera
- Przetestować inne modele LibraxisAI
- Skontaktować się z zespołem ws. Command A-03-2025