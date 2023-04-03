import { Component, OnInit } from '@angular/core';
import { MapProgress } from '../dto/map-progress';
import { ActivitiesService } from '../service/activities.service';
import { areas } from './area'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  active?: String;
  areas = areas;
  map_data: MapProgress[] = []
  progress?: MapProgress;
  

  constructor(private service: ActivitiesService) { }

  ngOnInit(): void {
    this.service.getProgressForMap().subscribe({
      next: (response: MapProgress[]) => this.onMapData(response)
    })
  }

  onMapData(response: MapProgress[]): void {
    this.map_data = response;
    for(let area of this.areas) {
      let progress = this.map_data.find(a => a.name === area.name);
      area.progress = progress ? String(progress.progress) : '0';
    }
  }

  ngAfterViewInit(): void {
  }

  show(area?: String) {
      this.active = area;
      this.progress = this.map_data.find(a => a.name === area);
  }


}
