import { useState } from "react";
import TodosRouterHanlder from "@/APICalls/TodosRouterHandler";
//@ts-ignore
export default function ToDoComponent({ setTrigeredEvent }) {
    const handler = TodosRouterHanlder.instance
    const [title, setTitle] = useState("")
    const [date, setDate] = useState("")
    const CREATE_TODO_URL = "http://127.0.0.1:8000/todos"

    const createToDo = () => {
        let todo
        if (date !== "") {
            todo = {
                "title": title,
                "due_date": date,
                "email": "aleks321@gmail.com" // It will be an actual email
            }
        }
        else {
            todo = {
                "title": title,
                "email": "aleks321@gmail.com" // It will be an actual email
            }
        }
        post(todo)
    }

    const post = async (todo: any) => {
        const isCreated = await handler.createTodo(new URL(CREATE_TODO_URL), todo)
        if (isCreated) {
            setTrigeredEvent(todo.title)
        }
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