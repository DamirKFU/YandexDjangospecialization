const curryearElement = document.getElementById("curryear");
const curdate = new Date(curryearElement.textContent);
const currDate = new Date();
const dateDiff = Math.abs((curdate - currDate) / (3600 * 1000));
if (dateDiff < 24) {
    curryearElement.textContent = String(currDate.getFullYear());
}
else {
    curryearElement.textContent = String(curdate.getFullYear());
}