# plaguss.github.io

Repository for my personal [website](https://plaguss.github.io/).

Built thanks to [hugo](https://gohugo.io/) and the theme [PaperMod](https://github.com/adityatelange/hugo-PaperMod/wiki/Features#regular-mode-default-mode).

## Kind reminders of the relevant commands:

Creating the site:

```sh
hugo new site plaguss.github.io
```

Get the theme (PaerMod in this case):

```sh
git clone https://github.com/adityatelange/hugo-PaperMod themes/PaperMod --depth=1
```

Run the server to see locally:

```sh
hugo server
```

To show posts marked with *draft*:

```sh
hugo server -D
```

Add a new post

```sh
hugo new blog/my-first-post.md
```

The deployment is automated, just push to the main branch and run.



