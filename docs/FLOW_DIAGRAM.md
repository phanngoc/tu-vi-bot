# Flow Diagram - New 3-Step Process

## Flow Overview

```
┌─────────────────┐
│   User Input    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Check Session  │
│   (Database)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Current Step?  │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌─────────┐
│ GREETING│ │COMPLETED│
└────┬────┘ └────┬────┘
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│ Step 1  │ │Follow-up│
│Extract  │ │Questions│
│ Name    │ │(Memory) │
└────┬────┘ └─────────┘
     │
     ▼
┌─────────┐
│ Step 2  │
│Extract  │
│All Info │
│(Memory  │
│Buffer)  │
└────┬────┘
     │
     ▼
┌─────────┐
│ Step 3  │
│Recognize│
│Enough   │
│Info     │
└────┬────┘
     │
     ▼
┌─────────┐
│Analysis │
│& Result │
└─────────┘
```

## Detailed Step Flow

### Step 1: Extract Name
```
User Message → Save to DB → Extract Name → Update Session → Response
     │              │            │              │
     ▼              ▼            ▼              ▼
"Tôi tên A" → chat_history → name_extraction → STEP_2 → "✅ Tên đã ghi nhận"
```

### Step 2: Extract All Info
```
User Message → Save to DB → Create Memory Buffer → Extract All Info → Check Complete
     │              │              │                    │
     ▼              ▼              ▼                    ▼
"15/03/1990" → chat_history → ChatSummaryMemory → name+date+time+gender → All Complete?
     │              │              │                    │
     ▼              ▼              ▼                    ▼
Response ← Update Session ← Update collected_info ← Yes: STEP_3 / No: Ask More
```

### Step 3: Recognize Enough Info
```
Auto Trigger → Check All Info → Generate Analysis → Save Result → Mark Complete
     │              │                │                │
     ▼              ▼                ▼                ▼
STEP_3 → All 4 fields? → fn_an_sao_comprehensive → chat_history → COMPLETED
```

## Database Schema

### Chat History Flow
```
chat_history table:
┌─────┬─────────┬──────────┬──────────┬─────────┬─────────────────┬─────────────┐
│ id  │ user_id │ message  │  role    │  step   │ extracted_info  │ created_at  │
├─────┼─────────┼──────────┼──────────┼─────────┼─────────────────┼─────────────┤
│  1  │ user123 │ "Xin chào"│  user   │ GREETING│      null       │ 2024-01-01  │
│  2  │ user123 │ "Tên A"  │  user   │STEP_1   │ {"name":"A"}    │ 2024-01-01  │
│  3  │ user123 │ "✅ Tên.."│assistant│STEP_2   │      null       │ 2024-01-01  │
│  4  │ user123 │ "15/03"  │  user   │STEP_2   │ {"date":"15/03"}│ 2024-01-01  │
│  5  │ user123 │ "🔮 Phân.."│assistant│COMPLETED│      null       │ 2024-01-01  │
└─────┴─────────┴──────────┴──────────┴─────────┴─────────────────┴─────────────┘
```

### User Session Flow
```
user_sessions table:
┌─────┬───────────┬──────────────┬─────────────────┬─────────────────┬─────────────┐
│ id  │session_id │ current_step │ collected_info  │ memory_summary  │ updated_at  │
├─────┼───────────┼──────────────┼─────────────────┼─────────────────┼─────────────┤
│  1  │  user123  │   GREETING   │       {}        │       ""        │ 2024-01-01  │
│  1  │  user123  │   STEP_2     │ {"name":"A"}    │       ""        │ 2024-01-01  │
│  1  │  user123  │   STEP_3     │ {"name":"A",    │ "User provided  │ 2024-01-01  │
│     │           │              │  "date":"15/03",│  name and date  │             │
│     │           │              │  "time":"14:30",│  information"   │             │
│     │           │              │  "gender":"Nam"}│                 │             │
│  1  │  user123  │  COMPLETED   │ {...}           │ "Full analysis  │ 2024-01-01  │
│     │           │              │                 │  completed"     │             │
└─────┴───────────┴──────────────┴─────────────────┴─────────────────┴─────────────┘
```

## Memory Buffer Integration

### ChatSummaryMemoryBuffer Process
```
1. Get chat_history from DB
2. Convert to ChatMessage format
3. Create ChatSummaryMemoryBuffer with:
   - LLM: gpt-4o-mini
   - Token limit: 2000
   - Tokenizer: tiktoken
4. Use for context-aware extraction
5. Update memory_summary in session
```

### Context Extraction
```
Previous Messages → Memory Buffer → Summarized Context → Better Extraction
     │                    │                │
     ▼                    ▼                ▼
"Tôi tên A"           ChatSummary      "User mentioned
"15/03/1990"      →   MemoryBuffer  →   name A and
"14:30"               (2000 tokens)      date 15/03"
"Nam"                                      │
                                          ▼
                                    More accurate
                                    extraction
```

## Error Handling

### Database Errors
- Connection issues → Fallback to in-memory
- Session not found → Create new session
- Data corruption → Reset session

### Memory Buffer Errors
- Token limit exceeded → Summarize older messages
- LLM errors → Fallback to simple extraction
- Context lost → Rebuild from database

### Extraction Errors
- Invalid format → Ask for clarification
- Missing info → Continue to next step
- Analysis failed → Show error message

## Performance Optimizations

1. **Database Indexing**: Index on user_id and created_at
2. **Memory Limit**: 2000 tokens for memory buffer
3. **Batch Operations**: Group database updates
4. **Caching**: Cache session data in memory
5. **Lazy Loading**: Load chat history only when needed
