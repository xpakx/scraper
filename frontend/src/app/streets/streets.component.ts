import { Component, OnInit } from '@angular/core';
import { Street } from '../dto/street';
import { ActivitiesService } from '../service/activities.service';

@Component({
  selector: 'app-streets',
  templateUrl: './streets.component.html',
  styleUrls: ['./streets.component.css']
})
export class StreetsComponent implements OnInit {
  streets: Street[] = [];

  constructor(private service: ActivitiesService) { }

  ngOnInit(): void {
    this.service.getStreets().subscribe({
      next: (response: Street[]) => this.onResponse(response)
    });
  }

  onResponse(response: Street[]): void {
    this.streets = response;
  }
}
