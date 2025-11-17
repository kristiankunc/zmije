import io
import tokenize

from internal.data import KEYWORD_MAP

# Keywords that are often used as variable names or are ambiguous
AMBIGUOUS_KEYWORDS = {("a",)}

def rewrite_tokens(tokens):
    buffer = []
    output = []
    paren_depth = 0  # Track parentheses depth
    after_def = False  # Track if we just saw 'def'
    in_def_parens = False  # Track if we're inside def() parameters
    after_dot = False  # Track if we just saw '.'

    for tok in tokens:
        # Track context
        if tok.type == tokenize.NAME and tok.string == "def":
            after_def = True
            in_def_parens = False
        
        if tok.type == tokenize.OP:
            if tok.string == "(":
                if after_def:
                    in_def_parens = True
                paren_depth += 1
            elif tok.string == ")":
                paren_depth -= 1
                if paren_depth == 0 and after_def:
                    in_def_parens = False
                    after_def = False
            elif tok.string == ".":
                after_dot = True
            elif tok.string not in (",", " "):
                after_dot = False
        
        if tok.type == tokenize.NAME:
            buffer.append(tok)
            
            # Check if we should replace this sequence
            should_replace = True
            
            # Don't replace if we're in function parameters
            if in_def_parens:
                should_replace = False
            
            # Don't replace if this is an attribute name (after a dot)
            if after_dot:
                should_replace = False
                after_dot = False
            
            # Don't replace ambiguous keywords (could be variable names)
            if should_replace:
                for keyword in AMBIGUOUS_KEYWORDS:
                    if len(buffer) >= len(keyword) and [t.string for t in buffer[-len(keyword):]] == list(keyword):
                        should_replace = False
                        break
            
            if should_replace:
                # try matching multi-word sequences (longest first)
                for seq in sorted(KEYWORD_MAP.keys(), key=len, reverse=True):
                    if len(buffer) >= len(seq):
                        window = buffer[-len(seq):]
                        if [t.string for t in window] == list(seq):
                            # Replace all tokens in the sequence with the first one containing the replacement
                            new = window[0]._replace(string=KEYWORD_MAP[seq])
                            buffer = buffer[:-len(seq)] + [new]
                            break
            continue

        # whenever a non-NAME arrives, flush everything
        while buffer:
            output.append(buffer.pop(0))
        output.append(tok)

    # flush at end
    while buffer:
        output.append(buffer.pop(0))
    
    return output

def replace_decimal_separator(tokens):
    """Replace , with . in decimal numbers"""
    output = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        
        # Check if this is a NUMBER token followed by a comma and another number
        if tok.type == tokenize.NUMBER and i + 2 < len(tokens):
            next_tok = tokens[i + 1]
            next_next_tok = tokens[i + 2]
            
            # If we have: NUMBER , NUMBER, replace the comma with dot
            if (next_tok.type == tokenize.OP and next_tok.string == "," and
                next_next_tok.type == tokenize.NUMBER):
                
                # Combine into a single NUMBER token with dot separator
                combined_string = tok.string + "." + next_next_tok.string
                new_tok = tok._replace(string=combined_string)
                output.append(new_tok)
                i += 3  # Skip the comma and next number token
                continue
        
        output.append(tok)
        i += 1
    
    return output

def replace_list_separators(tokens):
    """Replace ; with , for list separators to avoid confusion with floats"""
    output = []
    for tok in tokens:
        if tok.type == tokenize.OP and tok.string == ";":
            # Replace semicolon with comma for list/function argument separation
            new_tok = tok._replace(string=",")
            output.append(new_tok)
        else:
            output.append(tok)
    
    return output

def transpile(code):
    """
    Transpile Czech code to Python with safety checks.
    
    Transformations:
    1. Czech keywords to English keywords
    2. Decimal separator: , to .
    3. Czech quotes: „...‟ to "..."
    4. List separators: ; to ,
    """
    try:
        # Pre-process: Replace Czech quotes with regular quotes for tokenization
        code_normalized = code.replace('„', '"').replace('‟', '"')
        
        # Validate the normalized code can be tokenized
        tokens = list(tokenize.generate_tokens(io.StringIO(code_normalized).readline))
        
        # Apply transformations
        rewritten = rewrite_tokens(tokens)
        rewritten = replace_decimal_separator(rewritten)
        rewritten = replace_list_separators(rewritten)
        
        # Generate output
        result = tokenize.untokenize(rewritten)
        
        # Safety check: Ensure output is valid Python by attempting to compile
        try:
            compile(result, '<transpiled>', 'exec')
        except SyntaxError as e:
            print(f"Warning: Transpiled code may have syntax errors: {e}")
            print(f"Line {e.lineno}: {e.text}")
        
        return result
    
    except tokenize.TokenError as e:
        print(f"Error: Failed to tokenize code: {e}")
        raise
    except Exception as e:
        print(f"Error during transpilation: {e}")
        raise

with open("example.zm", "r", encoding="utf-8") as f:
    source_code = f.read()

transpiled_code = transpile(source_code)
with open("example.py", "w", encoding="utf-8") as f:
    f.write(transpiled_code)


