import MailHeader from "./MailHeader"

export default function Sidebar() {
    const arrayMails = [1, 2, 3, 4, 5, 6, 7, 8, 2, 2, 2, 2, 2, , 9, 9, 345]
    return (
        <aside className="col-span-3 bg-gray-50 dark:bg-gray-800 overflow-y-auto">
            <ul className="space-y-2 font-medium">
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
                <li className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                    <MailHeader />
                </li>
            </ul>
        </aside>
    )
}