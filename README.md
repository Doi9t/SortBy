## SortBy
*A Sublime Text plugin that allows you to sort lines with methods that are not present by default.*
- - -

### Sorting methods available
- Natural order
- Sort by the length of lines (Ascending / Descending)
	- Can be sorted alphabetically (Ascending / Descending) (Editable in SortBy.sublime-settings)
- Sort lines of text alphabetically (Ascending / Descending)
- Sort numbers numerically with and without surrounding caracters (Ascending / Descending)
    1. Binary
    2. Hexadecimal
    3. Decimal
    4. Octal

### Available features
1. Able to sort the entire file (when there is no selection)
2. Case sensitivity option for the alphabetically sort (Editable in SortBy.sublime-settings)

### Manual installation

1. Find your local Sublime Text [2, 3 or 4] Packages directory.
Example : `C:\Users\USER_NAME\AppData\Roaming\Sublime Text [2 or 3]\Packages`
2. Copy the SortBy directory inside the Packages directory.
3. Restart Sublime Text and enjoy !

### How to use
1. Select the text you want to sort.
2. Go in the menu "Tools", "Doi9t's packages" then you should see "SortBy".
3. Choose your option. (Either Reverse or normal).

Or using the control palette.
`CTRL` + `SHIFT` + `P` on Windows/Linux.
`COMMAND` + `SHIFT` + `P` on OS X.
and type SortBy in the box.

### Change the key binding
#### Create the file
1. In the `Preferences` menu
2. Go to `Package settings`
3. Go to `SortBy`
4. Click on `Key Bindings - User`

This will open / create a key bind file for the entire application.

#### Change the key binding
When the file is created or opened, you need to override the key binding that you want.

1. Copy the key binding from [Default.sublime-keymap](./Default.sublime-keymap) that you want to override (copy the entire JSON object).
**Example**
```json
  {
    "caption": "SortBy: Natural order",
    "keys": [
      "ctrl+shift+alt+q"
    ],
    "command": "srtbyli",
    "args": {
      "sort": "naturalOrder",
      "reversed": false
    }
  }
```
*In this example, the key bind is `ctrl+shift+alt+q`*

2. With the JSON object in your clipboard, add it to the created file, by making sure to wrap it in a JSON array (`[...]`).
**Example**
```json
[  
  {
    "caption": "SortBy: Natural order",
    "keys": [
      "ctrl+shift+alt+q"
    ],
    "command": "srtbyli",
    "args": {
      "sort": "naturalOrder",
      "reversed": false
    }
  }
]
```

3. Change the `keys` to the key binding that you want.


#### Disable the old key binding
If the old key binding is causing issues, you can disable it with the following JSON objet; just add it to the created file.
```json
  {
    "keys": [
      "ctrl+shift+alt+u"
    ],
    "command": "noop"
  }
```