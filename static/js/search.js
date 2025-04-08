// Search Function
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.querySelectorAll(".desktop-search-form, .mobile-search-form");

    searchForm.forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent page reload
            
            const query = this.querySelector("input[name='query']").value.toLowerCase().trim();
            
            // Page keywords to match against
            const pages = [
                { url: "/", keywords: ["home", "main", "welcome"] },
                { url: "/destinations", keywords: ["destinations", "places", "travel", "explore"] },
                { url: "/hotel_occupancy", keywords: ["hotel", "rates", "accommodation", "stay"] },
                { url: "/arrivals", keywords: ["arrivals", "tourists", "visitors", "stats"] }
            ];

            // Search logic
            const matchedPage = pages.find(page => 
                page.keywords.some(keyword => query.includes(keyword))
            );

            // Redirect or show 404 page
            if (matchedPage) {
                window.location.href = matchedPage.url;
            } else {
                window.location.href = "/404"; // Redirect to your custom 404 page
            }
        });
    });
});
