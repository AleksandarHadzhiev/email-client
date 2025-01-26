import { useState } from "react"

//@ts-ignore
export default function SendMessage({ setSendMessageIsActivated }) {

    const [to, setTo] = useState("")
    const [subject, setSubject] = useState("")
    const [body, setBody] = useState("")
    const SEND_URL = "http://localhost:8000/send"
    const username = localStorage.getItem("username") || ""

    // const [subject, setSubject] = useState("")

    const sendMessage = async () => {
        const message = {
            to: to,
            from: username,
            date: new Date().toLocaleString(),
            subject: subject,
            body: body
        }

        await fetch(SEND_URL, { method: "POST", body: JSON.stringify(message) }).then(async (res) => {
            const data = await res.json()
            console.log(data)
        }).catch((err) => {
            console.log(err)
        })
    }



    return (
        <section
            className="grid grid-rows-10 absolute bottom-0 right-0 bg-gray-900 text-white">
            <nav
                className="row-span-1">
                <div className="w-full bg-gray-800 grid grid-cols-10">
                    <button
                        className="hover:bg-red-500 bg-red-900 text-white w-4 rounded-sm"
                        onClick={() => { setSendMessageIsActivated(false) }}>
                        x
                    </button>
                    <label className="col-span-9">From: {username}</label>
                </div>
                <div className="mt-1 border-b-2 w-full grid grid-cols-10">
                    <label className="col-span-1">To:</label>
                    <input
                        className="bg-gray-900 text-white col-span-9"
                        type="email"
                        value={to}
                        onChange={e => { setTo(e.currentTarget.value); }}
                        placeholder="email@site.com" />
                </div>
            </nav>
            <main className="row-span-8">
                <input
                    className="bg-gray-900 text-white w-full mt-1 border-b-2"
                    placeholder="Subject.."
                    value={subject}
                    onChange={e => { setSubject(e.currentTarget.value); }} />
                <textarea
                    className="w-full h-full bg-gray-900 text-white mt-1"
                    placeholder="Hi, Mr./Mss. ..."
                    value={body}
                    onChange={e => { setBody(e.currentTarget.value); }}
                ></textarea>
            </main>
            <footer className="row-span-1 bg-gray-800 text-white grid grid-cols-10">
                <div className="col-span-8"></div>
                <button className="col-span-1 m-1" onClick={() => { sendMessage() }}>
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
            </footer>
        </section>
    )
}