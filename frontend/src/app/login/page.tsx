'use client'

import { useRouter } from "next/navigation";

export default function Index() {

    const router = useRouter()
    const BASE_URL = "http://127.0.0.1:8000/google/login"

    const fetchData = async () => {
        try {
            const res = await fetch(BASE_URL);
            const data = await res.json();
            router.push(data)
        } catch (err) {
            throw err;
        }
    }


    return (
        <div>
            <button onClick={() => { fetchData() }}>Google SSO</button>
        </div>
    )
}