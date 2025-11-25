#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:05:47 2025

@author: mikewoodward
"""

# %%---------------------------------------------------------------------------
# Module metadata
# -----------------------------------------------------------------------------
__author__ = "mikewoodward"
__license__ = "MIT"
__summary__ = "One line summary"

# %%---------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER, MSO_SHAPE_TYPE

if __name__ == "__main__":
    
    presentation = Presentation("Presentation1.pptx")

    # Extract the properties
    print("""Slide properties""")
    print("""================""")
    print(f"Title: {presentation.core_properties.title}")
    print(f"Author: {presentation.core_properties.author}")
    print(f"Created: {presentation.core_properties.created}")
    print(f"Modified: {presentation.core_properties.modified}")

    # Find and extract the footer
    print("""Slide footers""")
    print("""=============""")
    for slide in presentation.slides:
        # Iterate through shapes in each slide
        for shape in slide.shapes:
            # Check if the shape is a placeholder
            if shape.is_placeholder:
                # Check if the placeholder is a footer 
                if (shape.placeholder_format.type 
                    == PP_PLACEHOLDER.FOOTER):
                    # Get the footer text
                    footer_text = shape.text_frame.text
                    print(f"Slide "
                          f"{presentation.slides.index(slide) + 1} "
                          f"Footer: {footer_text}")

    # Find and extract all images
    print("""Slide images""")
    print("""============""")
    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                print("Found image")
                print("""Original file name """
                      """{shape.image.filename}""")
                print(f"""Image type {shape.image.content_type}""")
                print(f"""Image extension {shape.image.ext}""")
                print(f"""Image size {shape.image.size}""")
                print(f"""Image dpi {shape.image.dpi}""")

                with open(shape.image.filename, "wb") as f:
                    f.write(shape.image.blob)                
                
    # # Find and extract all notes
    print("""Slide notes""")
    print("""===========""")
    for slide in presentation.slides:
        if slide.has_notes_slide:
            print("""Notes for slide """
                  f"""{presentation.slides.index(slide) + 1}:""")
            print(slide.notes_slide.notes_placeholder.text)