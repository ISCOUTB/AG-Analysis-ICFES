export default function (id: string) {
    const element = document.getElementById(id);

    if (!element) return;

    element.scrollIntoView({ behavior: "smooth", block: "start" });
}
