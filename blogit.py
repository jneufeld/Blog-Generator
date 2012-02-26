import os
import sys
import datetime

# Constants
INSTALL_DIR     = "/home/jon/Programming/python/BlogTranslator/"
POSTS_PATH      = "posts/"
ABOUT_PAGE      = "about_archive.html"
BLOG_TITLE      = "null device"
BROWSER_TITLE   = "null device"

BLOG_DESCRIPTION = """I'm an undergraduate computer science student at UBC
Vancouver interested in operating systems, systems and network security, and
software engineering. <i>null device</i> is a way for me to track my thoughts
and progress -- as well as demonstrate a passion and expertise -- in these
areas.  """ 

# Each key represents a string from a text file to be translated, and each value
# is what it will be translated to. E.g., "[b]hello, fred[/b]" will become
# "<b>hello, fred</b>".
trans_table = {
        "[title]"   : "<h4>",
        "[/title]"  : "</h4>",

        "[b]"       : "<b>",
        "[/b]"      : "</b>",

        "[i]"       : "<i>",
        "[/i]"      : "</i>",

        "[p]"       : "<p>",
        "[/p]"      : "</p>",

        "[url="     : "<a href=",
        "\url]"        : ">",
        "[/url]"    : "</a>",

        "[gist="    : "<script src=\"http://gist.github.com/",
        "\gist]"    : ".js\"></script>",

        "[list]"    : "<ul>",
        "[/list]"   : "</ul>",
        "[li]"      : "<li>",
        "[/li]"     : "</li>"
    }

def translate(text_file):
    """ Take a text file written in user-specified markdown and turn it into a
        HTML file. """

    # Create the HTML of the blog post
    text = parse_markdown(text_file)
    date = make_timestamp()
    html = make_blog_html(text, date)

    # Write the post under an appropriate URL
    index = text_file.index(".txt")
    output_name = POSTS_PATH + date + "-" + text_file[:index] + ".html"
    output_file = open(output_name, "w")
    output_file.write(html)

    # Set this new blog post as the new index.html
    index_file = open(POSTS_PATH + "index.html", "w")
    index_file.write(html)

def make_timestamp():
    """ Get the current date and format it in YY/MM/DD as a string. """

    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")  

def parse_markdown(text_file):
    """ Go through a text file and replace all instances of markdown code with
        appropriate HTML. """ 

    text = ""
    input_file  = open(text_file, "r")
    for line in input_file:
        for markup in trans_table:
            line = line.replace(markup, trans_table[markup])
        text += line
    return text 

def make_blog_html(parsed_text, date):
    """ Create a HTML page with the parsed text as the body. """

    # Header contains title and CSS
    result = "<html>\n<head>\n<title>" + BROWSER_TITLE + "</title>\n"
    result += "<link rel=\"stylesheet\" type=\"text/css\""
    result += " href=\"stylesheets/custom.css\" />"
    result += "\n</head>\n<body>\n<center>\n\n"

    # Add the blog title
    result += "<div class=\"header\">\n"
    result += "<a href=\"about_archive.html\">"
    result += BLOG_TITLE
    result += "</a>"
    result += "\n</div>\n"
    result += "<hr \>"

    # Body contains user's post
    result += "\n<div class=\"post\">\n"
    result += parsed_text
    result += "<p><i>" + "Posted on " + date + "</i></p>"
    result += "\n</div>"

    # Finally, close it off nicely
    result += "\n</center>\n</body>\n</html>"

    return result

def make_about_html(posts):
    """ Create an archive page with a blog description. """

    # Header contains title and CSS
    result = "<html>\n<head>\n<title>" + BROWSER_TITLE + " - About</title>\n"
    result += "<link rel=\"stylesheet\" type=\"text/css\""
    result += " href=\"stylesheets/custom.css\" />"
    result += "\n</head>\n<body>\n<center>\n\n"

    # Header for blog description
    result += "<div class=\"header\">\n"
    result += "About"
    result += "\n</div>\n"
    result += "<hr \>"

    # Blog description content -- currently has to be hardcoded :(
    result += "\n<div class=\"post\">\n"
    result += BLOG_DESCRIPTION
    result += "\n</div>\n\n<br />\n\n"

    # Header for blog archive 
    result += "\n<div class=\"header\">\n"
    result += "Archive"
    result += "\n</div>\n"
    result += "<hr \>"

    # Archive of blog posts, most recent at the top
    result += "\n<div class=\"post\">\n"
    posts.reverse()
    for post in posts:
        date = post[0]
        link = post[1]
        name = post[2]

        result += date + ": "
        result += "<a href=\"" + link + "\">"
        result += name + "</a> <br />\n" 
    result += "\n</div>\n"

    # Finally, close it off nicely
    result += "\n</center>\n</body>\n</html>"
    return result
    
def get_posts():
    """ Get a list of all posts in the blog. """

    files = os.listdir(INSTALL_DIR + POSTS_PATH)
    return files

def parse_posts(files):
    """ Parse posts into file name and date, eliminate non-post files. """

    result = []

    for post in files:
        link = post

        # Skip non-html files
        if link[len(link) - 5:] != ".html":
            continue

        # Skip archive (this) file
        if link == ABOUT_PAGE:
            continue 

        # Skip index page (it's already a post!)
        if link == "index.html":
            continue

        date = post[:10]
        name = post[11:len(post) - 5]
        name = name.replace("-", " ")
        result.append((date, link, name))

    return result

def archive():
    """ Create an archive page with a blog description. """

    # Get the HTML necessary for the archive page
    files = get_posts() 
    posts = parse_posts(files)
    html  = make_about_html(posts)

    # Write it!
    output_file = open(POSTS_PATH + ABOUT_PAGE, "w")
    output_file.write(html)

if __name__ == "__main__":
    """ Translate each given markup file into a blog post and update the
        archive. """

    args = sys.argv[1:]
    for arg in args:
        translate(arg)
    archive()
