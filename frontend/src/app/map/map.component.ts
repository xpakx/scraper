import { Component, OnInit } from '@angular/core';
import { areas } from './area'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  active?: String;
  areas = areas;

  constructor() { }

  ngOnInit(): void {
    
  }

  ngAfterViewInit(): void {
  }

  show(area?: String) {
      this.active = area;
  }


}
