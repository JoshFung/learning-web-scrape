import * as React from 'react'

function ButtonList(props: any) {
    return (
        <div className={"buttonList" + " " + props.visibility}> 
            <button className="infoButton">INFO</button>
            <button className="themeButton">THEMES</button>
        </div>
    )
}

export default function MainBar() {
    return (
        <>
            <header className="topBar">
                <ButtonList visibility="hidden"/>
                <div className="title">GPU TRACKER</div>
                <ButtonList/>
            </header>
            <hr className="topBarLine"/>
        </>
    );
}