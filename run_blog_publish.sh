#!/bin/bash
# Publish next 3 blog post drafts on Mon/Wed/Fri
cd /Users/rebelhawk/Documents/Claude/pod-design-generator
/Library/Developer/CommandLineTools/usr/bin/python3 generate_blog_posts.py --publish-batch 1 >> logs/blog_publish.log 2>&1
