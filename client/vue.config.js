module.exports = {
    outputDir: "../dist",

    // relative to outputDir
    assetsDir: "static",
    css: {
        loaderOptions: {
            scss: {
                data: `
                @import "@/assets/scss/_variables.scss";
                @import "@/assets/scss/_mixins.scss";
              `
            }
        }
    }
};