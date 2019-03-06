# External lib/framework dependencies in frontend

**Notice**: This list may contain some legacy codes, which means those files are no longer used in current project and need removing.

## Active

the dependencies listed below are all active right now, which means they are still being used in project

### `bootstrap`

- **description**

  basic style framework (require `jquery`)

- **files**
    - for `jquery`:

          js
             jquery-3.3.1.min.js
             jquery-3.3.1.slim.min.js

    - for `bootstrap`

          css
             bootstrap-grid.css
             bootstrap-grid.css.map
             bootstrap-grid.min.css
             bootstrap-grid.min.css.map
             bootstrap-reboot.css
             bootstrap-reboot.css.map
             bootstrap-reboot.min.css
             bootstrap-reboot.min.css.map
             bootstrap.css
             bootstrap.css.map
             bootstrap.min.css
             bootstrap.min.css.map

          js
             bootstrap.bundle.js
             bootstrap.bundle.js.map
             bootstrap.bundle.min.js
             bootstrap.bundle.min.js.map
             bootstrap.js
             bootstrap.js.map
             bootstrap.min.js
             bootstrap.min.js.map

- **sites**

    - [bootstrap official site](https://getbootstrap.com)
    - [bootstrap chinese document site](https://getbootstrap.com)
    - [jquery official site](https://jquery.com)

### `bootstrap-select`

- **description**

  advanced select elements, including search and more

- **files**

      css
         bootstrap-select.css
         bootstrap-select.css.map
         bootstrap-select.min.css

      js
      │  bootstrap-select.js
      │  bootstrap-select.js.map
      │  bootstrap-select.min.js
      │  defaults-zh_CN.min.js
      │
      └─i18n
            bootstrap-select-zh_CN.min.js

- **sites**

    - [official site](https://github.com/snapappointments/bootstrap-select)

### `bootstrap-fileinput`

- **description**

  advanced fileinput element, including multiple selection, multipule uploading, preview and more.

- **files**

      css
         fileinput.min.css

      js
      │  fileinput.min.js
      │
      └─i18n
          └─bootstrap-fileinput
                zh.js

- **sites**

    - [official site](https://github.com/kartik-v/bootstrap-fileinput)

### `parsleyjs`

- **description**

    forms validator, support basic validation and custom validation

- **files**

      js
      │  parsley.min.js
      │  parsley.min.js.map
      │
      └─i18n
           zh_cn.extra.js
           zh_cn.js

- **sites**

    - [official site](https://github.com/guillaumepotier/Parsley.js)

## Need Migration

the deps listed below may still be used in this project, but they are not recommended to keep using and need migration to newer deps.

### `bootstrap-validator`

- **description**

    old forms validator

- **files**

      js
         validator.min.js

- **sites**

    - [official site](https://github.com/1000hz/bootstrap-validator)

## Unknown

The exact functions of the files below are not clear. They might be introduced as dependencies of other libs. Don't touch it unless you figured out their roles in frontend codes.

    js
        piexif.min.js
        popper.min.js