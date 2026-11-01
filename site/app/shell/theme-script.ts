export const THEME_STORAGE_KEY = "ams-theme";

// First-party inline script for <head>: applies a stored manual theme before
// first paint so a reader who chose a theme sees no flash. Without a stored
// choice it does nothing and tokens.css follows the system preference.
export const themeScript = `(function(){try{var t=localStorage.getItem(${JSON.stringify(THEME_STORAGE_KEY)});if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();`;
