
namespace Commons {

    export const common_style      = () : string => {
        return `
        .primary-bg {
            background-color: #11B0EF;
        }
        
        .warning-gradient-bg {
            background: rgb(224,24,24);
            background: linear-gradient(90deg, rgba(255,160,0,1) 0%, rgba(255,190,0,1) 100%);
        }

        .leaflet-container {
            height: 50vh;
        }
        `
    }

    export const get_datepicker_style   = () : string => {
        return `
        @charset "UTF-8";
        .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__month-read-view--down-arrow,
        .react-datepicker__month-year-read-view--down-arrow, .react-datepicker__navigation-icon::before {
        border-color: #ccc;
        border-style: solid;
        border-width: 3px 3px 0 0;
        content: "";
        display: block;
        height: 9px;
        position: absolute;
        top: 6px;
        width: 9px;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle, .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle {
        margin-left: -4px;
        position: absolute;
        width: 0;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::before, .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::before, .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::after, .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::after {
        box-sizing: content-box;
        position: absolute;
        border: 8px solid transparent;
        height: 0;
        width: 1px;
        content: "";
        z-index: -1;
        border-width: 8px;
        left: -8px;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::before, .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::before {
        border-bottom-color: #aeaeae;
        }

        .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle {
        top: 0;
        margin-top: -8px;
        }
        .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::before, .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::after {
        border-top: none;
        border-bottom-color: #f0f0f0;
        }
        .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::after {
        top: 0;
        }
        .react-datepicker-popper[data-placement^=bottom] .react-datepicker__triangle::before {
        top: -1px;
        border-bottom-color: #aeaeae;
        }

        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle {
        bottom: 0;
        margin-bottom: -8px;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::before, .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::after {
        border-bottom: none;
        border-top-color: #fff;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::after {
        bottom: 0;
        }
        .react-datepicker-popper[data-placement^=top] .react-datepicker__triangle::before {
        bottom: -1px;
        border-top-color: #aeaeae;
        }

        .react-datepicker-wrapper {
        display: inline-block;
        padding: 0;
        border: 0;
        width: 100%;
        }

        .react-datepicker {
        font-family: "Helvetica Neue", helvetica, arial, sans-serif;
        font-size: 0.8rem;
        background-color: #fff;
        color: #000;
        border: 1px solid #aeaeae;
        border-radius: 0.3rem;
        display: inline-block;
        position: relative;
        }

        .react-datepicker--time-only .react-datepicker__triangle {
        left: 35px;
        }
        .react-datepicker--time-only .react-datepicker__time-container {
        border-left: 0;
        }
        .react-datepicker--time-only .react-datepicker__time,
        .react-datepicker--time-only .react-datepicker__time-box {
        border-bottom-left-radius: 0.3rem;
        border-bottom-right-radius: 0.3rem;
        }

        .react-datepicker__triangle {
        position: absolute;
        left: 50px;
        }

        .react-datepicker-popper {
        z-index: 1;
        }
        .react-datepicker-popper[data-placement^=bottom] {
        padding-top: 10px;
        }
        .react-datepicker-popper[data-placement=bottom-end] .react-datepicker__triangle, .react-datepicker-popper[data-placement=top-end] .react-datepicker__triangle {
        left: auto;
        right: 50px;
        }
        .react-datepicker-popper[data-placement^=top] {
        padding-bottom: 10px;
        }
        .react-datepicker-popper[data-placement^=right] {
        padding-left: 8px;
        }
        .react-datepicker-popper[data-placement^=right] .react-datepicker__triangle {
        left: auto;
        right: 42px;
        }
        .react-datepicker-popper[data-placement^=left] {
        padding-right: 8px;
        }
        .react-datepicker-popper[data-placement^=left] .react-datepicker__triangle {
        left: 42px;
        right: auto;
        }

        .react-datepicker__header {
        text-align: center;
        background-color: #f0f0f0;
        border-bottom: 1px solid #aeaeae;
        border-top-left-radius: 0.3rem;
        padding: 8px 0;
        position: relative;
        }
        .react-datepicker__header--time {
        padding-bottom: 8px;
        padding-left: 5px;
        padding-right: 5px;
        }
        .react-datepicker__header--time:not(.react-datepicker__header--time--only) {
        border-top-left-radius: 0;
        }
        .react-datepicker__header:not(.react-datepicker__header--has-time-select) {
        border-top-right-radius: 0.3rem;
        }

        .react-datepicker__year-dropdown-container--select,
        .react-datepicker__month-dropdown-container--select,
        .react-datepicker__month-year-dropdown-container--select,
        .react-datepicker__year-dropdown-container--scroll,
        .react-datepicker__month-dropdown-container--scroll,
        .react-datepicker__month-year-dropdown-container--scroll {
        display: inline-block;
        margin: 0 15px;
        }

        .react-datepicker__current-month,
        .react-datepicker-time__header,
        .react-datepicker-year-header {
        margin-top: 0;
        color: #000;
        font-weight: bold;
        font-size: 0.944rem;
        }

        .react-datepicker-time__header {
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        }

        .react-datepicker__navigation {
        align-items: center;
        background: none;
        display: flex;
        justify-content: center;
        text-align: center;
        cursor: pointer;
        position: absolute;
        top: 2px;
        padding: 0;
        border: none;
        z-index: 1;
        height: 32px;
        width: 32px;
        text-indent: -999em;
        overflow: hidden;
        }
        .react-datepicker__navigation--previous {
        left: 2px;
        }
        .react-datepicker__navigation--next {
        right: 2px;
        }
        .react-datepicker__navigation--next--with-time:not(.react-datepicker__navigation--next--with-today-button) {
        right: 85px;
        }
        .react-datepicker__navigation--years {
        position: relative;
        top: 0;
        display: block;
        margin-left: auto;
        margin-right: auto;
        }
        .react-datepicker__navigation--years-previous {
        top: 4px;
        }
        .react-datepicker__navigation--years-upcoming {
        top: -4px;
        }
        .react-datepicker__navigation:hover *::before {
        border-color: #a6a6a6;
        }

        .react-datepicker__navigation-icon {
        position: relative;
        top: -1px;
        font-size: 20px;
        width: 0;
        }
        .react-datepicker__navigation-icon--next {
        left: -2px;
        }
        .react-datepicker__navigation-icon--next::before {
        transform: rotate(45deg);
        left: -7px;
        }
        .react-datepicker__navigation-icon--previous {
        right: -2px;
        }
        .react-datepicker__navigation-icon--previous::before {
        transform: rotate(225deg);
        right: -7px;
        }

        .react-datepicker__month-container {
        float: left;
        }

        .react-datepicker__year {
        margin: 0.4rem;
        text-align: center;
        }
        .react-datepicker__year-wrapper {
        display: flex;
        flex-wrap: wrap;
        max-width: 180px;
        }
        .react-datepicker__year .react-datepicker__year-text {
        display: inline-block;
        width: 4rem;
        margin: 2px;
        }

        .react-datepicker__month {
        margin: 0.4rem;
        text-align: center;
        }
        .react-datepicker__month .react-datepicker__month-text,
        .react-datepicker__month .react-datepicker__quarter-text {
        display: inline-block;
        width: 4rem;
        margin: 2px;
        }

        .react-datepicker__input-time-container {
        clear: both;
        width: 100%;
        float: left;
        margin: 5px 0 10px 15px;
        text-align: left;
        }
        .react-datepicker__input-time-container .react-datepicker-time__caption {
        display: inline-block;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container {
        display: inline-block;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__input {
        display: inline-block;
        margin-left: 10px;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__input input {
        width: auto;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__input input[type=time]::-webkit-inner-spin-button,
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__input input[type=time]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__input input[type=time] {
        -moz-appearance: textfield;
        }
        .react-datepicker__input-time-container .react-datepicker-time__input-container .react-datepicker-time__delimiter {
        margin-left: 5px;
        display: inline-block;
        }

        .react-datepicker__time-container {
        float: right;
        border-left: 1px solid #aeaeae;
        width: 85px;
        }
        .react-datepicker__time-container--with-today-button {
        display: inline;
        border: 1px solid #aeaeae;
        border-radius: 0.3rem;
        position: absolute;
        right: -87px;
        top: 0;
        }
        .react-datepicker__time-container .react-datepicker__time {
        position: relative;
        background: white;
        border-bottom-right-radius: 0.3rem;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box {
        width: 85px;
        overflow-x: hidden;
        margin: 0 auto;
        text-align: center;
        border-bottom-right-radius: 0.3rem;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list {
        list-style: none;
        margin: 0;
        height: calc(195px + (1.7rem / 2));
        overflow-y: scroll;
        padding-right: 0;
        padding-left: 0;
        width: 100%;
        box-sizing: content-box;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item {
        height: 30px;
        padding: 5px 10px;
        white-space: nowrap;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item:hover {
        cursor: pointer;
        background-color: #f0f0f0;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item--selected {
        background-color: #216ba5;
        color: white;
        font-weight: bold;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item--selected:hover {
        background-color: #216ba5;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item--disabled {
        color: #ccc;
        }
        .react-datepicker__time-container .react-datepicker__time .react-datepicker__time-box ul.react-datepicker__time-list li.react-datepicker__time-list-item--disabled:hover {
        cursor: default;
        background-color: transparent;
        }

        .react-datepicker__week-number {
        color: #ccc;
        display: inline-block;
        width: 1.7rem;
        line-height: 1.7rem;
        text-align: center;
        margin: 0.166rem;
        }
        .react-datepicker__week-number.react-datepicker__week-number--clickable {
        cursor: pointer;
        }
        .react-datepicker__week-number.react-datepicker__week-number--clickable:hover {
        border-radius: 0.3rem;
        background-color: #f0f0f0;
        }

        .react-datepicker__day-names,
        .react-datepicker__week {
        white-space: nowrap;
        }

        .react-datepicker__day-names {
        margin-bottom: -8px;
        }

        .react-datepicker__day-name,
        .react-datepicker__day,
        .react-datepicker__time-name {
        color: #000;
        display: inline-block;
        width: 1.7rem;
        line-height: 1.7rem;
        text-align: center;
        margin: 0.166rem;
        }

        .react-datepicker__month--selected, .react-datepicker__month--in-selecting-range, .react-datepicker__month--in-range,
        .react-datepicker__quarter--selected,
        .react-datepicker__quarter--in-selecting-range,
        .react-datepicker__quarter--in-range {
        border-radius: 0.3rem;
        background-color: #216ba5;
        color: #fff;
        }
        .react-datepicker__month--selected:hover, .react-datepicker__month--in-selecting-range:hover, .react-datepicker__month--in-range:hover,
        .react-datepicker__quarter--selected:hover,
        .react-datepicker__quarter--in-selecting-range:hover,
        .react-datepicker__quarter--in-range:hover {
        background-color: #1d5d90;
        }
        .react-datepicker__month--disabled,
        .react-datepicker__quarter--disabled {
        color: #ccc;
        pointer-events: none;
        }
        .react-datepicker__month--disabled:hover,
        .react-datepicker__quarter--disabled:hover {
        cursor: default;
        background-color: transparent;
        }

        .react-datepicker__day,
        .react-datepicker__month-text,
        .react-datepicker__quarter-text,
        .react-datepicker__year-text {
        cursor: pointer;
        }
        .react-datepicker__day:hover,
        .react-datepicker__month-text:hover,
        .react-datepicker__quarter-text:hover,
        .react-datepicker__year-text:hover {
        border-radius: 0.3rem;
        background-color: #f0f0f0;
        }
        .react-datepicker__day--today,
        .react-datepicker__month-text--today,
        .react-datepicker__quarter-text--today,
        .react-datepicker__year-text--today {
        font-weight: bold;
        }
        .react-datepicker__day--highlighted,
        .react-datepicker__month-text--highlighted,
        .react-datepicker__quarter-text--highlighted,
        .react-datepicker__year-text--highlighted {
        border-radius: 0.3rem;
        background-color: #3dcc4a;
        color: #fff;
        }
        .react-datepicker__day--highlighted:hover,
        .react-datepicker__month-text--highlighted:hover,
        .react-datepicker__quarter-text--highlighted:hover,
        .react-datepicker__year-text--highlighted:hover {
        background-color: #32be3f;
        }
        .react-datepicker__day--highlighted-custom-1,
        .react-datepicker__month-text--highlighted-custom-1,
        .react-datepicker__quarter-text--highlighted-custom-1,
        .react-datepicker__year-text--highlighted-custom-1 {
        color: magenta;
        }
        .react-datepicker__day--highlighted-custom-2,
        .react-datepicker__month-text--highlighted-custom-2,
        .react-datepicker__quarter-text--highlighted-custom-2,
        .react-datepicker__year-text--highlighted-custom-2 {
        color: green;
        }
        .react-datepicker__day--selected, .react-datepicker__day--in-selecting-range, .react-datepicker__day--in-range,
        .react-datepicker__month-text--selected,
        .react-datepicker__month-text--in-selecting-range,
        .react-datepicker__month-text--in-range,
        .react-datepicker__quarter-text--selected,
        .react-datepicker__quarter-text--in-selecting-range,
        .react-datepicker__quarter-text--in-range,
        .react-datepicker__year-text--selected,
        .react-datepicker__year-text--in-selecting-range,
        .react-datepicker__year-text--in-range {
        border-radius: 0.3rem;
        background-color: #216ba5;
        color: #fff;
        }
        .react-datepicker__day--selected:hover, .react-datepicker__day--in-selecting-range:hover, .react-datepicker__day--in-range:hover,
        .react-datepicker__month-text--selected:hover,
        .react-datepicker__month-text--in-selecting-range:hover,
        .react-datepicker__month-text--in-range:hover,
        .react-datepicker__quarter-text--selected:hover,
        .react-datepicker__quarter-text--in-selecting-range:hover,
        .react-datepicker__quarter-text--in-range:hover,
        .react-datepicker__year-text--selected:hover,
        .react-datepicker__year-text--in-selecting-range:hover,
        .react-datepicker__year-text--in-range:hover {
        background-color: #1d5d90;
        }
        .react-datepicker__day--keyboard-selected,
        .react-datepicker__month-text--keyboard-selected,
        .react-datepicker__quarter-text--keyboard-selected,
        .react-datepicker__year-text--keyboard-selected {
        border-radius: 0.3rem;
        background-color: #bad9f1;
        color: rgb(0, 0, 0);
        }
        .react-datepicker__day--keyboard-selected:hover,
        .react-datepicker__month-text--keyboard-selected:hover,
        .react-datepicker__quarter-text--keyboard-selected:hover,
        .react-datepicker__year-text--keyboard-selected:hover {
        background-color: #1d5d90;
        }
        .react-datepicker__day--in-selecting-range:not(.react-datepicker__day--in-range,
        .react-datepicker__month-text--in-range,
        .react-datepicker__quarter-text--in-range,
        .react-datepicker__year-text--in-range),
        .react-datepicker__month-text--in-selecting-range:not(.react-datepicker__day--in-range,
        .react-datepicker__month-text--in-range,
        .react-datepicker__quarter-text--in-range,
        .react-datepicker__year-text--in-range),
        .react-datepicker__quarter-text--in-selecting-range:not(.react-datepicker__day--in-range,
        .react-datepicker__month-text--in-range,
        .react-datepicker__quarter-text--in-range,
        .react-datepicker__year-text--in-range),
        .react-datepicker__year-text--in-selecting-range:not(.react-datepicker__day--in-range,
        .react-datepicker__month-text--in-range,
        .react-datepicker__quarter-text--in-range,
        .react-datepicker__year-text--in-range) {
        background-color: rgba(33, 107, 165, 0.5);
        }
        .react-datepicker__month--selecting-range .react-datepicker__day--in-range:not(.react-datepicker__day--in-selecting-range,
        .react-datepicker__month-text--in-selecting-range,
        .react-datepicker__quarter-text--in-selecting-range,
        .react-datepicker__year-text--in-selecting-range),
        .react-datepicker__month--selecting-range .react-datepicker__month-text--in-range:not(.react-datepicker__day--in-selecting-range,
        .react-datepicker__month-text--in-selecting-range,
        .react-datepicker__quarter-text--in-selecting-range,
        .react-datepicker__year-text--in-selecting-range),
        .react-datepicker__month--selecting-range .react-datepicker__quarter-text--in-range:not(.react-datepicker__day--in-selecting-range,
        .react-datepicker__month-text--in-selecting-range,
        .react-datepicker__quarter-text--in-selecting-range,
        .react-datepicker__year-text--in-selecting-range),
        .react-datepicker__month--selecting-range .react-datepicker__year-text--in-range:not(.react-datepicker__day--in-selecting-range,
        .react-datepicker__month-text--in-selecting-range,
        .react-datepicker__quarter-text--in-selecting-range,
        .react-datepicker__year-text--in-selecting-range) {
        background-color: #f0f0f0;
        color: #000;
        }
        .react-datepicker__day--disabled,
        .react-datepicker__month-text--disabled,
        .react-datepicker__quarter-text--disabled,
        .react-datepicker__year-text--disabled {
        cursor: default;
        color: #ccc;
        }
        .react-datepicker__day--disabled:hover,
        .react-datepicker__month-text--disabled:hover,
        .react-datepicker__quarter-text--disabled:hover,
        .react-datepicker__year-text--disabled:hover {
        background-color: transparent;
        }

        .react-datepicker__month-text.react-datepicker__month--selected:hover, .react-datepicker__month-text.react-datepicker__month--in-range:hover, .react-datepicker__month-text.react-datepicker__quarter--selected:hover, .react-datepicker__month-text.react-datepicker__quarter--in-range:hover,
        .react-datepicker__quarter-text.react-datepicker__month--selected:hover,
        .react-datepicker__quarter-text.react-datepicker__month--in-range:hover,
        .react-datepicker__quarter-text.react-datepicker__quarter--selected:hover,
        .react-datepicker__quarter-text.react-datepicker__quarter--in-range:hover {
        background-color: #216ba5;
        }
        .react-datepicker__month-text:hover,
        .react-datepicker__quarter-text:hover {
        background-color: #f0f0f0;
        }

        .react-datepicker__input-container {
        position: relative;
        display: inline-block;
        width: 100%;
        }

        .react-datepicker__year-read-view,
        .react-datepicker__month-read-view,
        .react-datepicker__month-year-read-view {
        border: 1px solid transparent;
        border-radius: 0.3rem;
        position: relative;
        }
        .react-datepicker__year-read-view:hover,
        .react-datepicker__month-read-view:hover,
        .react-datepicker__month-year-read-view:hover {
        cursor: pointer;
        }
        .react-datepicker__year-read-view:hover .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__year-read-view:hover .react-datepicker__month-read-view--down-arrow,
        .react-datepicker__month-read-view:hover .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__month-read-view:hover .react-datepicker__month-read-view--down-arrow,
        .react-datepicker__month-year-read-view:hover .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__month-year-read-view:hover .react-datepicker__month-read-view--down-arrow {
        border-top-color: #b3b3b3;
        }
        .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__month-read-view--down-arrow,
        .react-datepicker__month-year-read-view--down-arrow {
        transform: rotate(135deg);
        right: -16px;
        top: 0;
        }

        .react-datepicker__year-dropdown,
        .react-datepicker__month-dropdown,
        .react-datepicker__month-year-dropdown {
        background-color: #f0f0f0;
        position: absolute;
        width: 50%;
        left: 25%;
        top: 30px;
        z-index: 1;
        text-align: center;
        border-radius: 0.3rem;
        border: 1px solid #aeaeae;
        }
        .react-datepicker__year-dropdown:hover,
        .react-datepicker__month-dropdown:hover,
        .react-datepicker__month-year-dropdown:hover {
        cursor: pointer;
        }
        .react-datepicker__year-dropdown--scrollable,
        .react-datepicker__month-dropdown--scrollable,
        .react-datepicker__month-year-dropdown--scrollable {
        height: 150px;
        overflow-y: scroll;
        }

        .react-datepicker__year-option,
        .react-datepicker__month-option,
        .react-datepicker__month-year-option {
        line-height: 20px;
        width: 100%;
        display: block;
        margin-left: auto;
        margin-right: auto;
        }
        .react-datepicker__year-option:first-of-type,
        .react-datepicker__month-option:first-of-type,
        .react-datepicker__month-year-option:first-of-type {
        border-top-left-radius: 0.3rem;
        border-top-right-radius: 0.3rem;
        }
        .react-datepicker__year-option:last-of-type,
        .react-datepicker__month-option:last-of-type,
        .react-datepicker__month-year-option:last-of-type {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        border-bottom-left-radius: 0.3rem;
        border-bottom-right-radius: 0.3rem;
        }
        .react-datepicker__year-option:hover,
        .react-datepicker__month-option:hover,
        .react-datepicker__month-year-option:hover {
        background-color: #ccc;
        }
        .react-datepicker__year-option:hover .react-datepicker__navigation--years-upcoming,
        .react-datepicker__month-option:hover .react-datepicker__navigation--years-upcoming,
        .react-datepicker__month-year-option:hover .react-datepicker__navigation--years-upcoming {
        border-bottom-color: #b3b3b3;
        }
        .react-datepicker__year-option:hover .react-datepicker__navigation--years-previous,
        .react-datepicker__month-option:hover .react-datepicker__navigation--years-previous,
        .react-datepicker__month-year-option:hover .react-datepicker__navigation--years-previous {
        border-top-color: #b3b3b3;
        }
        .react-datepicker__year-option--selected,
        .react-datepicker__month-option--selected,
        .react-datepicker__month-year-option--selected {
        position: absolute;
        left: 15px;
        }

        .react-datepicker__close-icon {
        cursor: pointer;
        background-color: transparent;
        border: 0;
        outline: 0;
        padding: 0 6px 0 0;
        position: absolute;
        top: 0;
        right: 0;
        height: 100%;
        display: table-cell;
        vertical-align: middle;
        }
        .react-datepicker__close-icon::after {
        cursor: pointer;
        background-color: #216ba5;
        color: #fff;
        border-radius: 50%;
        height: 16px;
        width: 16px;
        padding: 2px;
        font-size: 12px;
        line-height: 1;
        text-align: center;
        display: table-cell;
        vertical-align: middle;
        content: "×";
        }

        .react-datepicker__today-button {
        background: #f0f0f0;
        border-top: 1px solid #aeaeae;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
        padding: 5px 0;
        clear: left;
        }

        .react-datepicker__portal {
        position: fixed;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.8);
        left: 0;
        top: 0;
        justify-content: center;
        align-items: center;
        display: flex;
        z-index: 2147483647;
        }
        .react-datepicker__portal .react-datepicker__day-name,
        .react-datepicker__portal .react-datepicker__day,
        .react-datepicker__portal .react-datepicker__time-name {
        width: 3rem;
        line-height: 3rem;
        }
        @media (max-width: 400px), (max-height: 550px) {
        .react-datepicker__portal .react-datepicker__day-name,
        .react-datepicker__portal .react-datepicker__day,
        .react-datepicker__portal .react-datepicker__time-name {
            width: 2rem;
            line-height: 2rem;
        }
        }
        .react-datepicker__portal .react-datepicker__current-month,
        .react-datepicker__portal .react-datepicker-time__header {
        font-size: 1.44rem;
        }

        .react-datepicker__children-container {
        width: 13.8rem;
        margin: 0.4rem;
        padding-right: 0.2rem;
        padding-left: 0.2rem;
        height: auto;
        }

        .react-datepicker__aria-live {
        position: absolute;
        clip-path: circle(0);
        border: 0;
        height: 1px;
        margin: -1px;
        overflow: hidden;
        padding: 0;
        width: 1px;
        white-space: nowrap;
        }
        `
    }

    export const get_leaflet_style      = () : string => {
        return `
        /* required styles */

        .leaflet-pane,
        .leaflet-tile,
        .leaflet-marker-icon,
        .leaflet-marker-shadow,
        .leaflet-tile-container,
        .leaflet-pane > svg,
        .leaflet-pane > canvas,
        .leaflet-zoom-box,
        .leaflet-image-layer,
        .leaflet-layer {
            position: absolute;
            left: 0;
            top: 0;
            }
        .leaflet-container {
            overflow: hidden;
            }
        .leaflet-tile,
        .leaflet-marker-icon,
        .leaflet-marker-shadow {
            -webkit-user-select: none;
               -moz-user-select: none;
                    user-select: none;
              -webkit-user-drag: none;
            }
        /* Prevents IE11 from highlighting tiles in blue */
        .leaflet-tile::selection {
            background: transparent;
        }
        /* Safari renders non-retina tile on retina better with this, but Chrome is worse */
        .leaflet-safari .leaflet-tile {
            image-rendering: -webkit-optimize-contrast;
            }
        /* hack that prevents hw layers "stretching" when loading new tiles */
        .leaflet-safari .leaflet-tile-container {
            width: 1600px;
            height: 1600px;
            -webkit-transform-origin: 0 0;
            }
        .leaflet-marker-icon,
        .leaflet-marker-shadow {
            display: block;
            }
        /* .leaflet-container svg: reset svg max-width decleration shipped in Joomla! (joomla.org) 3.x */
        /* .leaflet-container img: map is broken in FF if you have max-width: 100% on tiles */
        .leaflet-container .leaflet-overlay-pane svg {
            max-width: none !important;
            max-height: none !important;
            }
        .leaflet-container .leaflet-marker-pane img,
        .leaflet-container .leaflet-shadow-pane img,
        .leaflet-container .leaflet-tile-pane img,
        .leaflet-container img.leaflet-image-layer,
        .leaflet-container .leaflet-tile {
            max-width: none !important;
            max-height: none !important;
            width: auto;
            padding: 0;
            }
        
        .leaflet-container.leaflet-touch-zoom {
            -ms-touch-action: pan-x pan-y;
            touch-action: pan-x pan-y;
            }
        .leaflet-container.leaflet-touch-drag {
            -ms-touch-action: pinch-zoom;
            /* Fallback for FF which doesn't support pinch-zoom */
            touch-action: none;
            touch-action: pinch-zoom;
        }
        .leaflet-container.leaflet-touch-drag.leaflet-touch-zoom {
            -ms-touch-action: none;
            touch-action: none;
        }
        .leaflet-container {
            -webkit-tap-highlight-color: transparent;
        }
        .leaflet-container a {
            -webkit-tap-highlight-color: rgba(51, 181, 229, 0.4);
        }
        .leaflet-tile {
            filter: inherit;
            visibility: hidden;
            }
        .leaflet-tile-loaded {
            visibility: inherit;
            }
        .leaflet-zoom-box {
            width: 0;
            height: 0;
            -moz-box-sizing: border-box;
                 box-sizing: border-box;
            z-index: 800;
            }
        /* workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=888319 */
        .leaflet-overlay-pane svg {
            -moz-user-select: none;
            }
        
        .leaflet-pane         { z-index: 400; }
        
        .leaflet-tile-pane    { z-index: 200; }
        .leaflet-overlay-pane { z-index: 400; }
        .leaflet-shadow-pane  { z-index: 500; }
        .leaflet-marker-pane  { z-index: 600; }
        .leaflet-tooltip-pane   { z-index: 650; }
        .leaflet-popup-pane   { z-index: 700; }
        
        .leaflet-map-pane canvas { z-index: 100; }
        .leaflet-map-pane svg    { z-index: 200; }
        
        .leaflet-vml-shape {
            width: 1px;
            height: 1px;
            }
        .lvml {
            behavior: url(#default#VML);
            display: inline-block;
            position: absolute;
            }
        
        
        /* control positioning */
        
        .leaflet-control {
            position: relative;
            z-index: 800;
            pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
            pointer-events: auto;
            }
        .leaflet-top,
        .leaflet-bottom {
            position: absolute;
            z-index: 1000;
            pointer-events: none;
            }
        .leaflet-top {
            top: 0;
            }
        .leaflet-right {
            right: 0;
            }
        .leaflet-bottom {
            bottom: 0;
            }
        .leaflet-left {
            left: 0;
            }
        .leaflet-control {
            float: left;
            clear: both;
            }
        .leaflet-right .leaflet-control {
            float: right;
            }
        .leaflet-top .leaflet-control {
            margin-top: 10px;
            }
        .leaflet-bottom .leaflet-control {
            margin-bottom: 10px;
            }
        .leaflet-left .leaflet-control {
            margin-left: 10px;
            }
        .leaflet-right .leaflet-control {
            margin-right: 10px;
            }
        
        
        /* zoom and fade animations */
        
        .leaflet-fade-anim .leaflet-popup {
            opacity: 0;
            -webkit-transition: opacity 0.2s linear;
               -moz-transition: opacity 0.2s linear;
                    transition: opacity 0.2s linear;
            }
        .leaflet-fade-anim .leaflet-map-pane .leaflet-popup {
            opacity: 1;
            }
        .leaflet-zoom-animated {
            -webkit-transform-origin: 0 0;
                -ms-transform-origin: 0 0;
                    transform-origin: 0 0;
            }
        svg.leaflet-zoom-animated {
            will-change: transform;
        }
        
        .leaflet-zoom-anim .leaflet-zoom-animated {
            -webkit-transition: -webkit-transform 0.25s cubic-bezier(0,0,0.25,1);
               -moz-transition:    -moz-transform 0.25s cubic-bezier(0,0,0.25,1);
                    transition:         transform 0.25s cubic-bezier(0,0,0.25,1);
            }
        .leaflet-zoom-anim .leaflet-tile,
        .leaflet-pan-anim .leaflet-tile {
            -webkit-transition: none;
               -moz-transition: none;
                    transition: none;
            }
        
        .leaflet-zoom-anim .leaflet-zoom-hide {
            visibility: hidden;
            }
        
        
        /* cursors */
        
        .leaflet-interactive {
            cursor: pointer;
            }
        .leaflet-grab {
            cursor: -webkit-grab;
            cursor:    -moz-grab;
            cursor:         grab;
            }
        .leaflet-crosshair,
        .leaflet-crosshair .leaflet-interactive {
            cursor: crosshair;
            }
        .leaflet-popup-pane,
        .leaflet-control {
            cursor: auto;
            }
        .leaflet-dragging .leaflet-grab,
        .leaflet-dragging .leaflet-grab .leaflet-interactive,
        .leaflet-dragging .leaflet-marker-draggable {
            cursor: move;
            cursor: -webkit-grabbing;
            cursor:    -moz-grabbing;
            cursor:         grabbing;
            }
        
        /* marker & overlays interactivity */
        .leaflet-marker-icon,
        .leaflet-marker-shadow,
        .leaflet-image-layer,
        .leaflet-pane > svg path,
        .leaflet-tile-container {
            pointer-events: none;
            }
        
        .leaflet-marker-icon.leaflet-interactive,
        .leaflet-image-layer.leaflet-interactive,
        .leaflet-pane > svg path.leaflet-interactive,
        svg.leaflet-image-layer.leaflet-interactive path {
            pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
            pointer-events: auto;
            }
        
        /* visual tweaks */
        
        .leaflet-container {
            background: #ddd;
            outline-offset: 1px;
            }
        .leaflet-container a {
            color: #0078A8;
            }
        .leaflet-zoom-box {
            border: 2px dotted #38f;
            background: rgba(255,255,255,0.5);
            }
        
        
        /* general typography */
        .leaflet-container {
            font-family: "Helvetica Neue", Arial, Helvetica, sans-serif;
            font-size: 12px;
            font-size: 0.75rem;
            line-height: 1.5;
            }
        
        
        /* general toolbar styles */
        
        .leaflet-bar {
            box-shadow: 0 1px 5px rgba(0,0,0,0.65);
            border-radius: 4px;
            }
        .leaflet-bar a {
            background-color: #fff;
            border-bottom: 1px solid #ccc;
            width: 26px;
            height: 26px;
            line-height: 26px;
            display: block;
            text-align: center;
            text-decoration: none;
            color: black;
            }
        .leaflet-bar a,
        .leaflet-control-layers-toggle {
            background-position: 50% 50%;
            background-repeat: no-repeat;
            display: block;
            }
        .leaflet-bar a:hover,
        .leaflet-bar a:focus {
            background-color: #f4f4f4;
            }
        .leaflet-bar a:first-child {
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            }
        .leaflet-bar a:last-child {
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            border-bottom: none;
            }
        .leaflet-bar a.leaflet-disabled {
            cursor: default;
            background-color: #f4f4f4;
            color: #bbb;
            }
        
        .leaflet-touch .leaflet-bar a {
            width: 30px;
            height: 30px;
            line-height: 30px;
            }
        .leaflet-touch .leaflet-bar a:first-child {
            border-top-left-radius: 2px;
            border-top-right-radius: 2px;
            }
        .leaflet-touch .leaflet-bar a:last-child {
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
            }
        
        /* zoom control */
        
        .leaflet-control-zoom-in,
        .leaflet-control-zoom-out {
            font: bold 18px 'Lucida Console', Monaco, monospace;
            text-indent: 1px;
            }
        
        .leaflet-touch .leaflet-control-zoom-in, .leaflet-touch .leaflet-control-zoom-out  {
            font-size: 22px;
            }
        
        
        /* layers control */
        
        .leaflet-control-layers {
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            background: #fff;
            border-radius: 5px;
            }
        .leaflet-control-layers-toggle {
            background-image: url(images/layers.png);
            width: 36px;
            height: 36px;
            }
        .leaflet-retina .leaflet-control-layers-toggle {
            background-image: url(images/layers-2x.png);
            background-size: 26px 26px;
            }
        .leaflet-touch .leaflet-control-layers-toggle {
            width: 44px;
            height: 44px;
            }
        .leaflet-control-layers .leaflet-control-layers-list,
        .leaflet-control-layers-expanded .leaflet-control-layers-toggle {
            display: none;
            }
        .leaflet-control-layers-expanded .leaflet-control-layers-list {
            display: block;
            position: relative;
            }
        .leaflet-control-layers-expanded {
            padding: 6px 10px 6px 6px;
            color: #333;
            background: #fff;
            }
        .leaflet-control-layers-scrollbar {
            overflow-y: scroll;
            overflow-x: hidden;
            padding-right: 5px;
            }
        .leaflet-control-layers-selector {
            margin-top: 2px;
            position: relative;
            top: 1px;
            }
        .leaflet-control-layers label {
            display: block;
            font-size: 13px;
            font-size: 1.08333em;
            }
        .leaflet-control-layers-separator {
            height: 0;
            border-top: 1px solid #ddd;
            margin: 5px -10px 5px -6px;
            }
        
        /* Default icon URLs */
        .leaflet-default-icon-path { /* used only in path-guessing heuristic, see L.Icon.Default */
            background-image: url(images/marker-icon.png);
            }
        
        
        /* attribution and scale controls */
        
        .leaflet-container .leaflet-control-attribution {
            background: #fff;
            background: rgba(255, 255, 255, 0.8);
            margin: 0;
            }
        .leaflet-control-attribution,
        .leaflet-control-scale-line {
            padding: 0 5px;
            color: #333;
            line-height: 1.4;
            }
        .leaflet-control-attribution a {
            text-decoration: none;
            }
        .leaflet-control-attribution a:hover,
        .leaflet-control-attribution a:focus {
            text-decoration: underline;
            }
        .leaflet-attribution-flag {
            display: inline !important;
            vertical-align: baseline !important;
            width: 1em;
            height: 0.6669em;
            }
        .leaflet-left .leaflet-control-scale {
            margin-left: 5px;
            }
        .leaflet-bottom .leaflet-control-scale {
            margin-bottom: 5px;
            }
        .leaflet-control-scale-line {
            border: 2px solid #777;
            border-top: none;
            line-height: 1.1;
            padding: 2px 5px 1px;
            white-space: nowrap;
            -moz-box-sizing: border-box;
                 box-sizing: border-box;
            background: rgba(255, 255, 255, 0.8);
            text-shadow: 1px 1px #fff;
            }
        .leaflet-control-scale-line:not(:first-child) {
            border-top: 2px solid #777;
            border-bottom: none;
            margin-top: -2px;
            }
        .leaflet-control-scale-line:not(:first-child):not(:last-child) {
            border-bottom: 2px solid #777;
            }
        
        .leaflet-touch .leaflet-control-attribution,
        .leaflet-touch .leaflet-control-layers,
        .leaflet-touch .leaflet-bar {
            box-shadow: none;
            }
        .leaflet-touch .leaflet-control-layers,
        .leaflet-touch .leaflet-bar {
            border: 2px solid rgba(0,0,0,0.2);
            background-clip: padding-box;
            }
        
        
        /* popup */
        
        .leaflet-popup {
            position: absolute;
            text-align: center;
            margin-bottom: 20px;
            }
        .leaflet-popup-content-wrapper {
            padding: 1px;
            text-align: left;
            border-radius: 12px;
            }
        .leaflet-popup-content {
            margin: 13px 24px 13px 20px;
            line-height: 1.3;
            font-size: 13px;
            font-size: 1.08333em;
            min-height: 1px;
            }
        .leaflet-popup-content p {
            margin: 17px 0;
            margin: 1.3em 0;
            }
        .leaflet-popup-tip-container {
            width: 40px;
            height: 20px;
            position: absolute;
            left: 50%;
            margin-top: -1px;
            margin-left: -20px;
            overflow: hidden;
            pointer-events: none;
            }
        .leaflet-popup-tip {
            width: 17px;
            height: 17px;
            padding: 1px;
        
            margin: -10px auto 0;
            pointer-events: auto;
        
            -webkit-transform: rotate(45deg);
               -moz-transform: rotate(45deg);
                -ms-transform: rotate(45deg);
                    transform: rotate(45deg);
            }
        .leaflet-popup-content-wrapper,
        .leaflet-popup-tip {
            background: white;
            color: #333;
            box-shadow: 0 3px 14px rgba(0,0,0,0.4);
            }
        .leaflet-container a.leaflet-popup-close-button {
            position: absolute;
            top: 0;
            right: 0;
            border: none;
            text-align: center;
            width: 24px;
            height: 24px;
            font: 16px/24px Tahoma, Verdana, sans-serif;
            color: #757575;
            text-decoration: none;
            background: transparent;
            }
        .leaflet-container a.leaflet-popup-close-button:hover,
        .leaflet-container a.leaflet-popup-close-button:focus {
            color: #585858;
            }
        .leaflet-popup-scrolled {
            overflow: auto;
            }
        
        .leaflet-oldie .leaflet-popup-content-wrapper {
            -ms-zoom: 1;
            }
        .leaflet-oldie .leaflet-popup-tip {
            width: 24px;
            margin: 0 auto;
        
            -ms-filter: "progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678)";
            filter: progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678);
            }
        
        .leaflet-oldie .leaflet-control-zoom,
        .leaflet-oldie .leaflet-control-layers,
        .leaflet-oldie .leaflet-popup-content-wrapper,
        .leaflet-oldie .leaflet-popup-tip {
            border: 1px solid #999;
            }
        
        
        /* div icon */
        
        .leaflet-div-icon {
            background: #fff;
            border: 1px solid #666;
            }
        
        
        /* Tooltip */
        /* Base styles for the element that has a tooltip */
        .leaflet-tooltip {
            position: absolute;
            padding: 6px;
            background-color: #fff;
            border: 1px solid #fff;
            border-radius: 3px;
            color: #222;
            white-space: nowrap;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            pointer-events: none;
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
            }
        .leaflet-tooltip.leaflet-interactive {
            cursor: pointer;
            pointer-events: auto;
            }
        .leaflet-tooltip-top:before,
        .leaflet-tooltip-bottom:before,
        .leaflet-tooltip-left:before,
        .leaflet-tooltip-right:before {
            position: absolute;
            pointer-events: none;
            border: 6px solid transparent;
            background: transparent;
            content: "";
            }
        
        /* Directions */
        
        .leaflet-tooltip-bottom {
            margin-top: 6px;
        }
        .leaflet-tooltip-top {
            margin-top: -6px;
        }
        .leaflet-tooltip-bottom:before,
        .leaflet-tooltip-top:before {
            left: 50%;
            margin-left: -6px;
            }
        .leaflet-tooltip-top:before {
            bottom: 0;
            margin-bottom: -12px;
            border-top-color: #fff;
            }
        .leaflet-tooltip-bottom:before {
            top: 0;
            margin-top: -12px;
            margin-left: -6px;
            border-bottom-color: #fff;
            }
        .leaflet-tooltip-left {
            margin-left: -6px;
        }
        .leaflet-tooltip-right {
            margin-left: 6px;
        }
        .leaflet-tooltip-left:before,
        .leaflet-tooltip-right:before {
            top: 50%;
            margin-top: -6px;
            }
        .leaflet-tooltip-left:before {
            right: 0;
            margin-right: -12px;
            border-left-color: #fff;
            }
        .leaflet-tooltip-right:before {
            left: 0;
            margin-left: -12px;
            border-right-color: #fff;
            }
        
        /* Printing */
            
        @media print {
            /* Prevent printers from removing background-images of controls. */
            .leaflet-control {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
                }
            }
        `
    }


    export const derive_efficiency = (temperature:number, consumption:number, vibration:number, setup:any) : number => {
        let result                  = 100
        let normalized_percentage   = (min:number, max:number, curr:number) => {
            if (curr < min)
                return 0
            if (curr>max)
                return 1
            
            let n_max   = max-min
            let n_curr  = curr-min
    
            return n_curr/n_max
        }
        let n_t = normalized_percentage(setup.device.minTemperature, setup.device.maxTemperature, temperature)
        let n_c = normalized_percentage(setup.device.minPower, setup.device.maxPower, consumption)
        let n_v = normalized_percentage(setup.device.minVibration, setup.device.maxVibration, vibration)
        
        /*console.log (`n_% of ${temperature} among ${setup.device.minTemperature} and ${setup.device.maxTemperature} is ${n_t}`)
        console.log (`n_% of ${consumption} among ${setup.device.minPower} and ${setup.device.maxPower} is ${n_c}`)
        console.log (`n_% of ${vibration} among ${setup.device.minVibration} and ${setup.device.maxVibration} is ${n_v}`)*/
    
        return Number(((1-((n_t+n_c+n_v)/3))*100).toFixed(2))
    }
    
    
    const downsample = (a:any, p:number) => {
        let count   = Math.floor(a.length/100*p)
        let res     = []
        let step	= Math.floor(a.length/count)
        
        // console.log(count)
        // console.log (step)
    
        let tmp = step
        for (let i in a) {
                 if (tmp == 0)
              tmp= step/2
          else {
              tmp--
            res.push(a[i])
          }
        }
        
        return res
    }

};

export default Commons;