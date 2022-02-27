import * as React from 'react'
import ape from 'sony ape.jpg'
import SearchBar from './SearchBar';

export default function MainBody() {
    return (
        <view>
            <SearchBar/>
            <img src={ape} style={{height: '50%', width: '100%'}} alt="monkey"/>
        </view>
    );
}