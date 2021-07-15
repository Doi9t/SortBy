## SortBy
*A Sublime Text plugin that allows you to sort lines with methods that are not present by default.*
- - -

## Feature matrix
| Features                                   | ST2  | ST3  | ST4  | Description                                                                                                                                                              | 
|:------------------------------------------:|:----:|:----:|:----:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Natural order                              | x    | x    | x    | Sort the lines using the natural order, you can read more in an excellent article by [Jeff Atwood](https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/).|
| Sort by the length of lines                | x    | x    | x    |                                                                                                                                                                          |
| Sort lines of text alphabetically          | x    | x    | x    |                                                                                                                                                                          |
| Sort numbers numerically                   | x    | x    | x    |                                                                                                                                                                          |
| [Semantic Versioning](https://semver.org/) |      | x    | x    | Sort Semantic Versions, not supporting pre-releases / build metadata at the moment.                                                                                      |
| Regular expression                         |      | x    | x    | Sort the lines using a regex, to find the component and choose a subsort for the line.                                                                                   | 

You can check the [backward-incompatible-changes](./backward-incompatible-changes.md) file to see if you need to do something to keep your current settings / workflow.

1. Able to sort the entire file (when there is no selection)
2. Case sensitivity option for the `alphabetically sort` method (Editable in SortBy.sublime-settings)

## Installation

### With [Package Control](https://packagecontrol.io/packages/SortBy)
`CTRL` + `SHIFT` + `P` on Windows/Linux.
`COMMAND` + `SHIFT` + `P` on OS X.
and type SortBy in the box.

### Manual installation
1. Find your local Sublime Text `Packages` directory.
2. Copy the SortBy directory inside the Packages directory.
3. Restart Sublime Text and enjoy !

## How to use
1. Select the text you want to sort.
2. Go in the menu `Tools`, `Packages` then you should see `SortBy`.
3. Choose your option. (Either Reverse or normal).

## Settings
### Sorts
#### handle_selected_part_of_line_as_full_selected_line
Enable this (true) to ignore the start & end of the selection; any line that is touching the selection, will be sorted.

#### alphabetically_case_sensitive
Enable this (true) to sort with the case sensitivity (the lower and the upper cases will be sorted in two different groups).

#### Subsorts

##### Length of lines
*This Subsort is disabled by default.*

You can sort the line of the same length alphabetically.
To enable this subsort, add the `subsort_length_of_line` property with the value `ALPHABETICALLY` OR `ALPHABETICALLY_DESCENDING` in the plugin settings.

### Key Bindings
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
      "sort": "natural_order",
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
      "sort": "natural_order",
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