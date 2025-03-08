import RoutersHandler from "./routersHandler";

export default class TodosRouterHanlder {
    static #instance: TodosRouterHanlder;
    private constructor() { }

    public static get instance(): TodosRouterHanlder {
        if (!TodosRouterHanlder.#instance) {
            TodosRouterHanlder.#instance = new TodosRouterHanlder();
        }
        return TodosRouterHanlder.#instance
    }

    async getTodos(url: URL) {
        const routerHandler = new RoutersHandler(url, null)
        const body = await routerHandler.getHTTPMethod()
        // TODO: Check for todos in the response of the call ;)
        if ("todos" in body) {
            return body.todos
        }
        else {
            alert("Unexpected error, please try again later!")
        }
        return body
    }

    async createTodo(url: URL, data: any) {
        const routerHandler = new RoutersHandler(url, null)
        const body = await routerHandler.postHTTPMethod(data);
        return this.handleResponse(body)
    }

    handleResponse(body: any) {
        if ("message" in body) {
            alert(body.message)
            return true
        }
        else if ("error" in body) {
            alert(body.error.fail)
            return false
        }
        else {
            alert("Unexpected error, please try again later!")
            return false
        }
    }

    async updateTodo(url: URL, data: any) {
        const routerHandler = new RoutersHandler(url, null)
        const body = await routerHandler.putHTTPMethod(data);
        return this.handleResponse(body)
    }

    async deleteTodo(url: URL) {
        const routerHandler = new RoutersHandler(url, null)
        const body = await routerHandler.delteHTTPMethod();
        if (body == true) {
            alert("The task has been removed.")
            return true
        }
        else {
            alert("Fail, try again later.")
            return false
        }
    }
}