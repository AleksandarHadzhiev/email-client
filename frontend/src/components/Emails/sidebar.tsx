import { useState, useEffect } from "react"
import MailHeader from "./MailHeader"
import SendMessage from "./SendMessage"
import ExternalServiceHandler from "../../APICalls/ExternalServiceRouterHandler"
//@ts-ignore
export default function Sidebar({ setMail }) {
    const BASE_URL = "http://localhost:8000/get/mails"
    const [sendMessageIsActivated, setSendMessageIsActivated] = useState(false)
    const [mails, setMails] = useState([{ "from": "Aleks", "Date": "12.02.2024", "subject": "Renew contract", "body": "<p>Empty body</p>" }])
    useEffect(() => {
        const getMails = async () => {
            const externalServiceHandler = ExternalServiceHandler.instance
            const body = externalServiceHandler.getMails(new URL(BASE_URL))
            const data = await body
            setMails(data)
        }
        getMails()
    }, [mails.length])
    return (
        <aside className="col-span-3 bg-[#272727] bg-[#272727] overflow-y-auto">
            <button
                onClick={() => { setSendMessageIsActivated(true) }}
                type="button"
                className="flex m-2 bg-transparent hover:bg-blue-500 text-white font-semibold hover:text-white py-2 px-4 border border-solid border-2 border-white hover:border-transparent rounded">
                Send new message
                <svg
                    className="h-8 w-8 ml-2"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13" />
                    <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
            </button>
            <ul className="space-y-2 font-medium">
                {mails.map((email, index) => (

                    <li onClick={() => { setMail(email) }} key={index} className="border-b-2 border-t-2 border-gray-700 hover:bg-sky-400">
                        {email !== null ? <MailHeader email={email} /> : null}
                    </li>
                ))}
            </ul>
            {sendMessageIsActivated ? <SendMessage setSendMessageIsActivated={setSendMessageIsActivated} /> : null}
        </aside>
    )
}