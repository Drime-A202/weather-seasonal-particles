from stlitepack import pack

pack(
    app_file="app.py",
    extra_files=[
        "config.py",
        "weather_api.py",
        "term_mapping.py",
        "canvas_builder.py"
    ]
)