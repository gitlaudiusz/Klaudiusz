# MLX Models Cheatsheet

## Working Models & Configs

### Command A-03-2025
- **Port**: 53173 lub 8555
- **Endpoint**: `/v1/chat/completions`
- **CRITICAL**: Nie podawaj nazwy modelu!
- **Speed**: ~2 min dla długich odpowiedzi
- **Good for**: Deep knowledge, philosophy

### Nemotron Super 49B
- **Port**: 8555 (production)
- **Endpoint**: `/v1/chat/completions`
- **Speed**: ~1 min responses
- **RAM**: ~50GB
- **Good for**: Fast, structured responses

### Nemotron Ultra 253B
- **Status**: ⚠️ Problematic (timeouts, tokenizer issues)
- **RAM**: ~175GB
- **Speed**: 3.86 tokens/sec (bardzo wolny)
- **Has patches folder**: USE-IF-MODEL-FAILED-TO-GENERATE/

## MLX Server Management

```bash
# Start server (proper way)
cd /Users/polyversai/Codebase/Klaudiusz/mlx_lm
nohup uv run mlx_lm.server --model /path/to/model --host 0.0.0.0 --port PORT --trust-remote-code > model.log 2>&1 &

# Save PID for safe management
ps aux | grep "port PORT" | grep -v grep | awk '{print $2}' > model_pid.txt

# Kill specific server
kill $(cat model_pid.txt)
```

## Golden Rules
1. **NEVER** use `pkill -f` - kills innocent processes
2. **ALWAYS** save PIDs before operations
3. **NEVER** include model name in c4ai requests
4. Copy MLX environment locally, don't use ~/.lmstudio paths