export default class RoutersHandler {
    private body: any = null

    constructor(private url: URL, private token: any) {
    }

    setBodyToBeSend(data: any) {
        this.body = data
    }

    async getHTTPMethod() {
        let headers = undefined
        if (this.token && this.body) {
            headers = {
                'access_token': this.body.access_token,
                'csrf': this.token,
                'refresh_token': this.body.refresh_token,
                'expires_in': this.body.expires_in,
                'type': this.body.type
            }
        }
        else if (this.token && this.body === null) {
            headers = { 'csrf': this.token }
        }

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