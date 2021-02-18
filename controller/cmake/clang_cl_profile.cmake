function(set_compiler_profile)
    add_compile_options(/EHsc)
    add_compile_options(/clang:-fbracket-depth=1024)
    add_compile_options(/clang:-Wall /clang:-Wextra)      # -Wpedantic will usually trigger thousands of warnings in library code.
    add_compile_options(/clang:-Wno-unknown-attributes)   # Mute warnings due to lack of C++20 attribute support.
    add_compile_options(/clang:-Wno-unused-parameter)
endfunction()