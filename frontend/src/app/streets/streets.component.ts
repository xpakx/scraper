import { Component, OnInit } from '@angular/core';
import { Progress } from '../dto/progress';
import { Street } from '../dto/street';
import { ActivitiesService } from '../service/activities.service';

@Component({
  selector: 'app-streets',
  templateUrl: './streets.component.html',
  styleUrls: ['./streets.component.css']
})
export class StreetsComponent implements OnInit {
  streets: Street[] = [];
  page: number = 0;
  progress?: Progress;

  constructor(private service: ActivitiesService) { }

  ngOnInit(): void {
    this.service.getStreets().subscribe({
      next: (response: Street[]) => this.onResponse(response)
    });
    this.service.getProgress().subscribe({
      next: (response: Progress) => this.onProgressResponse(response)
    });
  }

  onResponse(response: Street[]): void {
    this.streets = response;
  }

  onProgressResponse(response: Progress): void {
    this.progress = response;
  }

  nextPage(): void {
    this.getPage(++this.page);
  }

  prevPage(): void {
    if(this.page > 0) {
      this.getPage(--this.page);
    }
  }

  getPage(page: number): void {
    this.service.getStreets(page).subscribe({
      next: (response: Street[]) => this.onResponse(response)
    });
  }
}
