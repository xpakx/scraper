import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.css']
})
export class ProgressBarComponent implements OnInit {
  @Input() percentage: String = '0%';
  @Input() total: number = 0;
  @Input('completed') completed_streets: number = 0;
  @Input() finished: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

}
