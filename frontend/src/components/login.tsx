'use client'

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Login() {

    const router = useRouter()
    const [email, setEmail] = useState("")
    const LOGIN_URL = "http://127.0.0.1:8000/login"

    const post = async () => {
        console.log(email)
        await fetch(LOGIN_URL, { method: "POST", body: JSON.stringify({ email: email }) }).then(async (res) => {
            const data = await res.json()

            router.push(data.redirect)
        }).catch((err) => {
            console.log(err)
        })
    }

    return (
        <div className="w-full h-screen flex justify-center items-center align-center">
            <div className="flex flex-col w-48 space-y-6">
                <div>
                    <img src="data:image/png;base64,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"></img>
                </div>
                <div className="max-w-sm bg-transparent">
                    <label className="block text-sm font-medium mb-2">Email</label>
                    <input
                        type="email"
                        id="input-label"
                        className="bg-transparent py-3 px-4 block w-full border-solid border-2 border-white rounded-lg text-sm focus:border-white focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                        placeholder="you@site.com"
                        value={email}
                        onChange={e => { setEmail(e.currentTarget.value); }}
                    />
                </div>
                <button
                    className="bg-transparent hover:bg-blue-500 text-white font-semibold hover:text-white py-2 px-4 border border-solid border-2 border-white hover:border-transparent rounded"
                    onClick={() => { post() }}
                >Continue
                </button>
            </div>
        </div>
    )
}