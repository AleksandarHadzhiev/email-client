export default class RoutersHandler {

    constructor(private url: URL, private token: any) {
    }

    async getHTTPMethod() {
        const headers = this.token ? { 'csrf': this.token } : undefined
        const res = await fetch(this.url, { method: "GET", headers: headers }).then(async (res) => {
            const status = res.status
            if (status == 200) {
                return await res.json()
            }
            else {
                return await res.json()
            }
        }).catch((err) => { alert(err) })
        return res
    }

    async postHTTPMethod(data: any) {
        const res = await fetch(this.url, { method: "POST", body: JSON.stringify(data), headers: { 'csrf': this.token } })
            .then(async (res) => {
                const status = res.status
                if (status == 200) {
                    return await res.json()
                }
                else {
                    return await res.json()
                }
            }).catch((err) => {
                alert(err)
            });
        return res;
    }

    async delteHTTPMethod() {
        const res = await fetch(this.url, { method: "DELETE" }).then(async (res) => {
            const status = res.status
            if (status == 200) {
                return true
            }
            else {
                return false
            }
        }).catch((err) => {
            alert(err)
        });
        return res;
    }

    async putHTTPMethod(data: any) {
        const res = await fetch(this.url, { method: "PUT", body: JSON.stringify(data) })
            .then(async (res) => {
                const status = res.status
                if (status == 200) {
                    return await res.json()
                }
                else {
                    return await res.json()
                }
            }).catch((err) => {
                alert(err)
            });
        return res;
    }
}