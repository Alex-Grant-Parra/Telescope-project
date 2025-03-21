from flask import Blueprint, jsonify, render_template
from models.tables import HDSTARtable, IndexTable, NGCtable

star_map_bp = Blueprint("star_map", __name__)

@star_map_bp.route("/api/stars")
def get_stars():
    all_stars = []
    tables = [HDSTARtable, IndexTable, NGCtable]

    for table in tables:
        stars = table.query.all()
        for star in stars:
            try:
                # Check if RA or DEC is None and handle it
                ra_value = star.RA if star.RA is not None else 0  # Default to 0 if None
                dec_value = star.DEC if star.DEC is not None else 0  # Default to 0 if None

                # Convert RA (hours) to degrees, handle potential None
                ra_decimal = float(ra_value) * 15  # Convert RA from hours to degrees
                dec_decimal = float(dec_value)     # DEC is already in degrees

                # Handle V-Mag (Visual Magnitude) with getattr() in case it is missing
                v_mag = getattr(star, "V-Mag", 0)  # Default to 0 if V-Mag is None

                all_stars.append({
                    "name": getattr(star, "Name"),  # Correctly fetch "Name" column
                    "ra": ra_decimal,   # Right Ascension in degrees
                    "dec": dec_decimal, # Declination in degrees
                    "mag": v_mag        # Visual Magnitude
                })
            except Exception as e:
                print(f"Error processing star {getattr(star, 'Name', 'UNKNOWN')}: {e}")

    return jsonify(all_stars)

@star_map_bp.route("/StarMap")
def star_map():
    all_stars = []
    tables = [HDSTARtable, IndexTable, NGCtable]

    for table in tables:
        stars = table.query.all()
        for star in stars:
            try:
                # Check if RA or DEC is None and handle it
                ra_value = star.RA if star.RA is not None else 0
                dec_value = star.DEC if star.DEC is not None else 0
                
                ra_decimal = float(ra_value) * 15  # Convert RA from hours to degrees
                dec_decimal = float(dec_value)

                v_mag = getattr(star, "V-Mag", 0)  # Default to 0 if V-Mag is None

                all_stars.append({
                    "name": getattr(star, "Name"),
                    "ra": ra_decimal,
                    "dec": dec_decimal,
                    "mag": v_mag
                })
            except Exception as e:
                print(f"Error processing star {getattr(star, 'Name', 'UNKNOWN')}: {e}")

    return render_template("star_map.html", stars=all_stars)
