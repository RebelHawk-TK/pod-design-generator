#!/bin/bash
# Publish blog post drafts — tripled to 6 per run
# Schedule: Mon/Wed/Fri at 2:00 AM
cd /Users/rebelhawk/Documents/Claude/pod-design-generator
/Library/Developer/CommandLineTools/usr/bin/python3 generate_blog_posts.py --publish-batch 6 >> logs/blog_publish.log 2>&1
