/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'sherwood': {
                    '50': '#ebfef5',
                    '100': '#cffce5',
                    '200': '#a4f6d1',
                    '300': '#69ecb9',
                    '400': '#2ed99c',
                    '500': '#09c084',
                    '600': '#009c6c',
                    '700': '#007d5a',
                    '800': '#026349',
                    '900': '#034d3a',
                    '950': '#002e23',
                },
                'rope': {
                    '50': '#fefcec',
                    '100': '#fcf4c9',
                    '200': '#f8e78f',
                    '300': '#f5d654',
                    '400': '#f2c32d',
                    '500': '#eba515',
                    '600': '#d07e0f',
                    '700': '#ad5a10',
                    '800': '#8a4513',
                    '900': '#743a13',
                    '950': '#421d06',
                },
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
