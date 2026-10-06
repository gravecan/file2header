import os
import re
import sys

SUPPORTED_EXTENSIONS = (".png", ".gif", ".ttf")


def file2h( file_path ):
    if not os.path.isfile( file_path ):
        print( f"File not found: {file_path}" )
        return

    if not file_path.lower().endswith( SUPPORTED_EXTENSIONS ):
        print( "Only PNG, GIF and TTF files are supported." )
        return

    filename = os.path.basename( file_path )
    name = os.path.splitext( filename )[0]

    var_name = re.sub( r'[^a-zA-Z0-9_]', '_', name )

    if var_name[0].isdigit():
        var_name = "_" + var_name

    with open( file_path, "rb" ) as f:
        data = f.read()

    output_path = os.path.join( os.path.dirname( file_path ), f"{name}.h" )

    with open( output_path, "w", encoding="utf-8" ) as f:
        f.write( "#pragma once\n\n" )
        f.write( f"inline unsigned char {var_name}[] = {{\n" )

        for i in range( 0, len( data ), 16 ):
            chunk = data[i:i + 16]

            hex_values = ", ".join( f"0x{byte:02X}" for byte in chunk )
            f.write( f"    {hex_values}" )

            if i + 16 < len( data ):
                f.write( "," )

            f.write( "\n" )
        f.write( "};\n\n" )
        f.write( f"inline unsigned int {var_name}_size = {len( data )};\n" )

    print( f"File: {file_path}" )
    print( f"Header: {output_path}" )
    print( f"Size: {len( data )} bytes" )


if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print( "Usage :" )
        print( "python file2h.py v.png" )
        print( "python file2h.py v.gif" )
        print( "python file2h.py v.ttf" )
        sys.exit( 1 )

    file2h( sys.argv[1] )
