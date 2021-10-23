#!/usr/bin/env python3
from wand.image import Image
import argparse

def generate_text(text, outputName, text_color='#fff'):
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
    textImage.save(filename=outputName)

def main():
    parser = argparse.ArgumentParser(description='Fill this desc later.')
    parser.add_argument('type', choices=['text'], help='The type of image for the tool to generate. Can be one of: text', metavar='type')
    parser.add_argument('-string', required=True, help='The content of the generated text.')
    parser.add_argument('-color', help='The color of the generated text in hexadecimal format.', default="#fff")
    parser.add_argument('-output', help='Filename of the result image.', required=True)
    
    args = parser.parse_args()

    if args.type == 'text':
        generate_text(args.string, args.color, args.output)

main()