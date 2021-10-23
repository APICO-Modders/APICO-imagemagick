#!/usr/bin/env python3
from wand.image import Image
import argparse

def generate_text(text, output_name, text_color='#fff'):
    '''Creates an image using a spritefont from a string.'''
    text = text.replace(' ', '_').lower()

    textImage = Image()
    for c in text:
        # For every character in the string, append the right spritefont to the sequence of frames
        textImage.sequence.append(Image(filename='font/font-{0}.png'.format(c)))

    # Draw out every frame in the sequence side by side
    textImage.concat()

    # Apply the specified color to the whole text sprite, with no transparency
    textImage.colorize(color=text_color, alpha='#fff')
    textImage.save(filename=output_name)

def draw_outline(original, outline_color='#fffffe'):
    '''Creates an image that consists of only the outline of an original input image.'''
    sprite = original.clone()
    
    # Draw the outer edge of the image. Diamond kernel is the one that appears to work the best for it
    sprite.morphology(method='edgeout', kernel='diamond')

    # Change the color of the outer edge
    sprite.colorize(color=outline_color, alpha='#fff')
    return sprite

def draw_blank(original, blank_color='#121d35'):
    '''Creates an image that is a "blank" single color version of the original input image. Used in APICO for undiscovered items.'''
    sprite = original.clone()

    # Apply a single color to the whole image
    sprite.colorize(color=blank_color, alpha='#fff')
    return sprite

def generate_spritesheet(input_name, add_darkoutline, output_name):
    '''Takes a single sprite and creates a whole spritesheet to use in APICO.
    The spritesheet will include the original sprite, and its undiscovered and mouseover versions.'''
    spritesheet = Image()
    with Image(filename=input_name) as sprite:
        # If the sprite has no dark outline, used by all sprites in APICO, draw that one first
        if add_darkoutline == True:
            dark_outline = draw_outline(sprite, "#121d35")
            sprite.composite(dark_outline)

        # Get the outline of the sprite and add it on top of a copy of the sprite
        outline = draw_outline(sprite)
        with_outline = sprite.clone()
        with_outline.composite(outline)

        # Get the undiscovered version of the sprite
        blank = draw_blank(sprite)

        # Apply the outline of the sprite to a copy of the undiscovered version
        blank_with_outline = blank.clone()
        blank_with_outline.composite(outline)

        # Add the original sprite and all its versions to a sequence of frames in the spritesheet
        spritesheet.sequence.append(sprite)    
        spritesheet.sequence.append(with_outline)
        spritesheet.sequence.append(blank)
        spritesheet.sequence.append(blank_with_outline)
    
    # Draw out every frame in the sequence side by side
    spritesheet.concat()
    spritesheet.save(filename=output_name)

def main():
    parser = argparse.ArgumentParser(description='Fill this desc later.')
    parser.add_argument('type', choices=['text', 'spritesheet'], help='The type of image for the tool to generate. Can be one of: text, spritesheet.', metavar='type')
    parser.add_argument('-string', help='The content of the generated text. Used with the "text" type.')
    parser.add_argument('-color', help='The color of the generated text in hexadecimal format. Used with the "text" type.', default="#fff")
    parser.add_argument('-sprite', help='Input sprite to generate a spritesheet with outlines and blank images from. Used with the "spritesheet" type.')
    parser.add_argument('-darkoutline', help='Draw a dark outline around the sprite in addition to the light hover outline', default=False, type=bool)
    parser.add_argument('-output', help='Filename of the result image.', required=True)
    
    args = parser.parse_args()

    if args.type == 'text':
        generate_text(args.string, args.output, args.color)
    if args.type == 'spritesheet':
        generate_spritesheet(args.sprite, args.darkoutline, args.output)

main()