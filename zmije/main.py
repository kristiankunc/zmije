import io
import tokenize
import keyword

from zmije.internal.data import KEYWORD_MAP

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
                    if len(buffer) >= len(keyword) and [t.string.lower() for t in buffer[-len(keyword):]] == [k.lower() for k in keyword]:
                        should_replace = False
                        break
            
            if should_replace:
                # try matching multi-word sequences (longest first)
                for seq in sorted(KEYWORD_MAP.keys(), key=len, reverse=True):
                    if len(buffer) >= len(seq):
                        window = buffer[-len(seq):]
                        # Case-insensitive comparison
                        if [t.string.lower() for t in window] == [k.lower() for k in seq]:
                            # Replace all tokens in the sequence with the first one containing the replacement
                            # Preserve the original casing for the first character
                            replacement = KEYWORD_MAP[seq]
                            new = window[0]._replace(string=replacement)
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

def validate_variables_capitalized(code):
    """
    Validate that all variables start with capital letters.
    
    Only checks variables being assigned (NAME = ...), not function definitions
    or other uses of names. Excludes attribute assignments (obj.attr = ...).
    """    
    # Python keywords (def, if, for, etc.)
    python_keywords = set(keyword.kwlist)
    
    # Czech keywords that will be transpiled to English
    czech_keywords = set()
    for key in KEYWORD_MAP.keys():
        if isinstance(key, tuple):
            czech_keywords.add(key[0])
        else:
            czech_keywords.add(key)
    
    # Built-in functions and types
    builtin_names = set(dir(__builtins__) if isinstance(__builtins__, dict) else dir(__builtins__))
    
    code_normalized = code.replace('„', '"').replace('‟', '"')
    # Strip leading/trailing whitespace to normalize line numbers
    code_normalized = code_normalized.strip()
    
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code_normalized).readline))
    except tokenize.TokenError as e:
        # Re-raise tokenization errors (e.g., invalid variable names)
        raise ValueError(f"Invalid code: {e}")
    
    # Try to compile to catch syntax errors early
    try:
        compile(code_normalized, '<validate>', 'exec')
    except SyntaxError as e:
        # Raise as ValueError for consistency with validation errors
        raise ValueError(f"Invalid code: {e}")
    
    # Look for variables being assigned: NAME = ...
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        
        # Check for assignment: NAME = ...
        if (tok.type == tokenize.NAME and 
            i + 1 < len(tokens) and 
            tokens[i + 1].type == tokenize.OP and 
            tokens[i + 1].string == "="):
            
            # Check if this is an attribute assignment (has a dot before it)
            # Look back to see if there's a dot before this NAME
            is_attribute = False
            if i > 0 and tokens[i - 1].type == tokenize.OP and tokens[i - 1].string == ".":
                is_attribute = True
            
            # Skip attribute assignments
            if is_attribute:
                i += 1
                continue
            
            # This is a variable assignment
            var_name = tok.string
            if (var_name not in python_keywords and
                var_name not in czech_keywords and
                var_name not in builtin_names and
                var_name and
                not var_name[0].isupper()):
                raise ValueError(
                    f"Variable '{var_name}' at line {tok.start[0]}, column {tok.start[1]} "
                    f"does not start with a capital letter. All variables must be capitalized."
                )
        
        i += 1

def validate_no_english_keywords(code):
    """
    Validate that the source code does not contain English keywords that have Czech translations.
    Raises ValueError if English keywords are found.
    """
    # Extract all English keywords (values from KEYWORD_MAP)
    english_keywords = set(value for value in KEYWORD_MAP.values())
    
    # Tokenize the code to check for NAME tokens
    code_normalized = code.replace('„', '"').replace('‟', '"')
    tokens = list(tokenize.generate_tokens(io.StringIO(code_normalized).readline))
    
    for tok in tokens:
        if tok.type == tokenize.NAME and tok.string in english_keywords:
            raise ValueError(
                f"Found English keyword '{tok.string}' at line {tok.start[0]}, column {tok.start[1]}. "
                f"This keyword has a Czech translation. Use the Czech version instead. "
                f"Source code should be written entirely in Czech."
            )

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
        # Validate that all variables are capitalized
        validate_variables_capitalized(code)
        
        # Validate that no English keywords are used
        validate_no_english_keywords(code)
        
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
    
    except ValueError as e:
        print(f"Validation Error: {e}")
        raise
    except tokenize.TokenError as e:
        print(f"Error: Failed to tokenize code: {e}")
        raise
    except Exception as e:
        print(f"Error during transpilation: {e}")
        raise

if __name__ == "__main__":
    with open("example.zm", "r", encoding="utf-8") as f:
        source_code = f.read()

    transpiled_code = transpile(source_code)
    with open("example.py", "w", encoding="utf-8") as f:
        f.write(transpiled_code)


