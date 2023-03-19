import { Component, OnInit } from '@angular/core';
import { Activity } from '../dto/activity';
import { ActivitiesService } from '../service/activities.service';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.css']
})
export class ActivitiesComponent implements OnInit {
  activities: Activity[] = [];

  constructor(private service: ActivitiesService) { }

  ngOnInit(): void {
    this.service.getActivities().subscribe({
      next: (response: Activity[]) => this.onResponse(response)
    });
  }

  onResponse(response: Activity[]): void {
    this.activities = response;
  }

}
