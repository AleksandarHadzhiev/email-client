import { useRef, useState } from 'react';
import ExternalServiceHandler from '@/app/ExternalServiceRouterHandler';

//@ts-ignore
export default function SendMessage({ setSendMessageIsActivated }) {
    const externalExerivceHandler = ExternalServiceHandler.instance
    const [to, setTo] = useState("")
    const [subject, setSubject] = useState("")
    const [body, setBody] = useState("")
    const SEND_URL = "http://localhost:8000/send"
    const username = localStorage.getItem("username") || ""
    const fileInput = useRef<HTMLInputElement>(null)
    let _files: {}[] = []

    async function uploadAttachment(e: React.ChangeEvent<HTMLInputElement>) {
        const files = e.target.files
        const file = files ? files[0] : null
        if (file != null) {
            const fileReader = new FileReader()
            fileReader.readAsBinaryString(file)
            fileReader.onload = e => {
                const content = e.target?.result
                const _file = {
                    name: file.name,
                    type: file.type,
                    content: content
                }
                _files.push(_file)
            }
        }
    }

    const sendMessage = async () => {
        let message = {}
        if (_files.length == 0) {
            message = {
                to: to,
                from: username,
                date: new Date().toLocaleString(),
                subject: subject,
                body: body,
            }
        }
        else {
            message = {
                to: to,
                from: username,
                date: new Date().toLocaleString(),
                subject: subject,
                body: body,
                attachments: _files
            }
        }

        const res = await externalExerivceHandler.sendMessage(message, new URL(SEND_URL))
        if (res == 'SENT') {
            setSendMessageIsActivated(false)
            alert("Success")
        }
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
                <div
                    className="col-span-1 flex items-center justify-between hover:text-blue-400">
                    <label htmlFor="file-upload">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                        </svg></label>
                    <input
                        onChange={uploadAttachment}
                        ref={fileInput}
                        style={{ display: 'none' }}
                        type="file"
                        id="file-upload"
                        multiple />
                </div>
                <div className="col-span-7"></div>
                <button className="col-span-1 flex items-center justify-between hover:text-blue-400" onClick={() => { sendMessage() }}>
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