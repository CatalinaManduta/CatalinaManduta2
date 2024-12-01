// Use existing TOC script
document.addEventListener("DOMContentLoaded", function() {
    const tocList = document.getElementById("toc-list");
    const headings = document.querySelectorAll(".content-wrapper h3");
    headings.forEach((heading, index) => {
        if (!heading.id) heading.id = `section${index + 1}`;
        const tocItem = document.createElement("li");
        const tocLink = document.createElement("a");
        tocLink.href = `#${heading.id}`;
        tocLink.textContent = heading.textContent;
        tocItem.appendChild(tocLink);
        tocList.appendChild(tocItem);
    });
});
