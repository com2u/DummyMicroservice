<ul class="livestats">
    <li>
        <span class="title">Queries<br />Blocked</span>
        <strong>{!! $ads_blocked_today !!}</strong>
    </li>
    <li>
        <span class="title">Queries<br />Blocked</span>
	<strong>{!! $data_progress !!}</strong> 
    </li>

    <li>
        <span class="title">Percent<br /> Blocked</span>
        <strong>{!! $ads_percentage_today !!}</strong>
        <label>Copy:<progress id="fortschritt" value="{!! $data_progress !!}" max="3"></progress></label>
    </li>
</ul>
