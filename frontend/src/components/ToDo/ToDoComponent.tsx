import { useState } from "react";

//@ts-ignore
export default function ToDoComponent({ setTrigeredEvent }) {
    const [title, setTitle] = useState("")
    const [desc, setDesc] = useState("")
    const [date, setDate] = useState("")
    const CREATE_TODO_URL = "http://127.0.0.1:8000/todos"

    const createToDo = () => {
        const todo = {
            "title": title,
            "description": desc,
            "due_date": date,
            "email": "aleks321@gmail.com" // It will be an actual email
        }
        post(todo)
    }

    const post = async (todo: { title: string; description: string; due_date: string; email: string }) => {
        await fetch(CREATE_TODO_URL, { method: "POST", body: JSON.stringify(todo) }).then(async (res) => {
            if (res.status != 201) {
                alert(res)
            }
            else {
                const data = await res.json()
                setTrigeredEvent("added")
            }
        }).catch((err) => {
            alert(err)
        })
    }

    return (
        <div className="flex bg-[#272727] h-12 items-center align-center">
            <button
                className="flex bg-transparent text-white font-semibold hover:text-gray-400 border border-solid border-2 border-white hover:border-gray-400 rounded py-1 px-3 rounded-full ml-2 mr-2"
                onClick={() => {
                    createToDo()
                }}>+</button>
            <div className="rounded-md w-full">
                <input
                    className="w-full rounded-md bg-transparent border-2 border-gray-200 text-white text-center"
                    placeholder="Title.."
                    value={title}
                    onChange={e => { setTitle(e.currentTarget.value); }} />
            </div>
            <div className="">
                <input
                    id="dueDate"
                    className="bg-transparent text-gray-200 border-2 rounded-md mr-2 ml-2"
                    datepicker-format="mm-dd-yyyy"
                    type="date"
                    value={date}
                    onChange={e => { setDate(e.currentTarget.value); }}
                />
            </div>
        </div >
    )
}